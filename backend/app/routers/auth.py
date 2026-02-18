from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.config import settings
from app.models.account import Account, Token
from app.integrations.threads_client import ThreadsClient
import httpx
import logging

router = APIRouter(prefix="/auth/threads", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/start")
async def start_auth():
    """Generates the authorization URL for Threads."""
    base_url = "https://www.threads.net/oauth/authorize"
    params = {
        "client_id": settings.THREADS_CLIENT_ID,
        "redirect_uri": settings.THREADS_REDIRECT_URI,
        "scope": settings.THREADS_SCOPES,
        "response_type": "code"
    }
    # Construct URL manually to ensure correct encoding/format if needed, or return params
    auth_url = f"{base_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}&response_type=code"
    return {"url": auth_url}

@router.get("/status")
async def get_auth_status(db: Session = Depends(get_db)):
    """Returns the current connection status."""
    token = db.query(Token).first()
    if not token or not token.access_token:
        return {
            "connected": False,
            "username": None,
            "threads_user_id": None,
            "expires_at": None,
            "scopes": []
        }
    
    try:
        # Get account info
        account = db.query(Account).filter(Account.id == token.account_id).first()
        username = account.username if account else None
        
        return {
            "connected": True,
            "username": username,
            "threads_user_id": account.threads_user_id if account else None,
            "expires_at": None, # Stored tokens don't have explicit expiry in this simple schema yet
            "scopes": settings.get_scopes_list()
        }
    except Exception as e:
        logger.error(f"Error in status endpoint: {e}")
        return {
             "connected": False,
             "username": None,
             "threads_user_id": None,
             "expires_at": None,
             "scopes": []
        }

@router.get("/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    """Exchanges the authorization code for an access token."""
    
    # Exchange code for token
    token_url = "https://graph.threads.net/oauth/access_token"
    # IMPORTANT: Redirect URI must match exactly what was sent in the authorization request
    data = {
        "client_id": settings.THREADS_CLIENT_ID,
        "client_secret": settings.THREADS_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": settings.THREADS_REDIRECT_URI,
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to exchange token: {e}")
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")

    access_token = token_data.get("access_token")
    user_id = token_data.get("user_id") # Threads often returns user_id here too

    if not access_token:
         raise HTTPException(status_code=400, detail="No access token received")

    # Fetch user details to create/update account
    threads_client = ThreadsClient(access_token=access_token)
    try:
        user_info = await threads_client.get_me()
    except Exception as e:
         logger.error(f"Failed to fetch user info: {e}")
         raise HTTPException(status_code=400, detail="Failed to fetch user info from Threads")
    
    # Update/Create Account
    account = db.query(Account).filter(Account.threads_user_id == user_info.get("id")).first()
    if not account:
        account = Account(
            threads_user_id=user_info.get("id"),
            username=user_info.get("username")
        )
        db.add(account)
        db.commit()
        db.refresh(account)
    
    # Store/Update Token
    # In a real app, handle multiple tokens or update existing
    token = db.query(Token).filter(Token.account_id == account.id).first()
    if not token:
        token = Token(
            account_id=account.id,
            access_token=access_token,
            scopes=settings.THREADS_SCOPES
        )
        db.add(token)
    else:
        token.access_token = access_token
    
    db.commit()

    db.commit()

    from fastapi.responses import RedirectResponse
    # Redirect to configured frontend URL
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/connect?connected=true&username={account.username}")
