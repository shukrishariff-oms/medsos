import httpx
from typing import Optional, Dict, Any, List
from app.core.config import settings

class IntegrationError(Exception):
    def __init__(self, message: str, status_code: int = 500, raw: dict = None):
        self.message = message
        self.status_code = status_code
        self.raw = raw
        super().__init__(message)

class ThreadsClient:
    def __init__(self, access_token: str):
        self.base_url = settings.THREADS_GRAPH_BASE
        self.base_url = "https://graph.threads.net" # Changed from settings.THREADS_GRAPH_BASE
        self.access_token = access_token
        # self.headers removed as httpx.AsyncClient handles it
        self.client = httpx.AsyncClient(headers={"Authorization": f"Bearer {access_token}"}) # New: httpx client initialized here

    async def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> Dict[str, Any]: # Signature changed: added params
        url = f"{self.base_url}{endpoint}"
        try:
            # Using self.client and json=data for POST/PUT, params=params for GET
            if method.upper() == "GET":
                response = await self.client.request(method, url, params=params)
            else:
                response = await self.client.request(method, url, json=data)
            if response.status_code >= 400:
                error_data = None
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", "Unknown error")
                except ValueError: # Catch JSON decoding errors
                    error_msg = response.text
                raise IntegrationError(f"Threads API Error: {error_msg}", status_code=response.status_code, raw=error_data)
            response.raise_for_status() # Keep this for other HTTP errors not caught by the 400 check
            return response.json()
        except httpx.RequestError as e: # Catch network-related errors
            raise IntegrationError(f"Network error: {str(e)}") from e
        except httpx.HTTPStatusError as e: # Catch remaining HTTP status errors (e.g., 3xx redirects, 5xx if not caught by 400 check)
            error_data = None
            try:
                error_data = e.response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
            except ValueError:
                error_msg = e.response.text
            raise IntegrationError(f"Threads API Error: {error_msg}", status_code=e.response.status_code, raw=error_data) from e
        except Exception as e: # Catch any other unexpected errors
            raise IntegrationError(f"An unexpected error occurred: {str(e)}") from e

    async def get_me(self) -> Dict[str, Any]:
        return await self._request("GET", "/me?fields=id,username,name,threads_profile_picture_url,threads_biography")

    async def get_user_threads(self, user_id: str) -> List[Dict[str, Any]]:
        # fields might be needed, but for now basic
        response = await self._request("GET", f"/v1.0/{user_id}/threads?fields=id,media_product_type,media_type,shortcode,text,timestamp,username,permalink")
        return response.get("data", [])

    async def create_text_post(self, text: str, user_id: str):
        data = {
            "media_type": "TEXT",
            "text": text
        }
        # Step 1: Create container
        container = await self._request("POST", f"/v1.0/{user_id}/threads", data)
        container_id = container.get("id")

        # Step 2: Publish
        publish_data = {"creation_id": container_id}
        result = await self._request("POST", f"/v1.0/{user_id}/threads_publish", publish_data)
        return result.get("id")

    async def delete_post(self, media_id: str):
         # Threads API currently docs are limited on DELETE for external tools, 
         # but if it exists it would be DELETE /media_id
         # For now, we assume it might not work or return 200
         pass

    async def list_replies(self, media_id: str) -> List[Dict[str, Any]]:
        response = await self._request("GET", f"/{media_id}/replies", params={
            "fields": "id,text,username,timestamp,permalink"
        })
        return response.get("data", [])

    async def reply(self, text: str, parent_media_id: str, user_id: str) -> str:
        # Step 1: Create a media container (reply)
        container_data = await self._request("POST", f"/v1.0/{user_id}/threads", data={
             "media_type": "TEXT",
             "text": text,
             "reply_to_id": parent_media_id
        })
        creation_id = container_data.get("id")

        # Step 2: Publish
        publish_data = await self._request("POST", f"/v1.0/{user_id}/threads_publish", data={
            "creation_id": creation_id
        })
        return publish_data.get("id")

    async def get_insights(self, media_id: str) -> Dict[str, Any]:
        # Placeholder metrics. Threads API insights might require specific metrics params
        metrics = "views,likes,replies,reposts,quotes" 
        response = await self._request("GET", f"/{media_id}/insights", params={
            "metric": metrics
        })
        return response.get("data", [])
