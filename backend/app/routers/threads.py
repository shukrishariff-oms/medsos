from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.account import Token, Account
from app.models.post import Post as PostModel
from app.models.reply import Reply as ReplyModel
from app.models.insights import InsightsSnapshot
from app.schemas.post import PostCreate, Post
from app.schemas.reply import ReplyCreate, Reply
from app.schemas.insights import InsightsSnapshot as InsightsSchema
from app.integrations.threads_client import ThreadsClient
import logging

router = APIRouter(prefix="/threads", tags=["threads"])
logger = logging.getLogger(__name__)

def get_threads_client(db: Session = Depends(get_db)) -> ThreadsClient:
    # Single user assumption: get the first available token
    token = db.query(Token).first()
    if not token or not token.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No connected Threads account found. Please connect first."
        )
    return ThreadsClient(access_token=token.access_token)

async def get_current_user_id(db: Session = Depends(get_db)) -> str:
    token = db.query(Token).first()
    if not token:
        raise HTTPException(status_code=401, detail="Not connected")
    account = db.query(Account).filter(Account.id == token.account_id).first()
    if not account:
         raise HTTPException(status_code=401, detail="Account not found")
    return account.threads_user_id

@router.get("/me")
async def get_me(client: ThreadsClient = Depends(get_threads_client)):
    return await client.get_me()

@router.get("/my-posts")
async def get_my_posts(
    client: ThreadsClient = Depends(get_threads_client),
    user_id: str = Depends(get_current_user_id)
):
    try:
        return await client.get_user_threads(user_id)
    except Exception as e:
        logger.error(f"Failed to fetch posts: {e}")
        # Return empty list on error to not break frontend completely if API is strict
        return []

@router.get("/posts", response_model=List[Post])
async def list_posts(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    from app.services.post_service import PostService
    service = PostService(db)
    return service.list_posts(limit=limit)

@router.post("/post", response_model=Post)
async def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    client: ThreadsClient = Depends(get_threads_client),
    user_id: str = Depends(get_current_user_id)
):
    from app.services.post_service import PostService
    from app.integrations.threads_client import IntegrationError
    service = PostService(db)
    
    # Create PENDING/DRAFT record
    db_post = service.create_post_record(post.text, status="PENDING")

    try:
        media_id = await client.create_text_post(post.text, user_id=user_id)
        # Update to PUBLISHED
        return service.mark_published(db_post.id, media_id)
    except IntegrationError as e:
        logger.error(f"Threads API Error: {e.message}")
        return service.mark_failed(db_post.id, e.message)
    except Exception as e:
        logger.error(f"Unexpected error publishing post: {e}")
        return service.mark_failed(db_post.id, str(e))

@router.delete("/post/{media_id}")
async def delete_post(
    media_id: str,
    db: Session = Depends(get_db),
    client: ThreadsClient = Depends(get_threads_client)
):
    from app.services.post_service import PostService
    service = PostService(db)
    
    # Try to delete from Threads
    try:
        await client.delete_post(media_id)
    except Exception as e:
        logger.warning(f"Failed to delete from Threads API: {e}")

    # Mark deleted in DB
    result = service.mark_deleted_by_media_id(media_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found locally")
        
    return {"ok": True}

@router.get("/post/{media_id}/replies", response_model=List[dict])
async def list_replies(
    media_id: str,
    client: ThreadsClient = Depends(get_threads_client)
):
    try:
        replies = await client.list_replies(media_id)
        return replies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reply")
async def reply_to_post(
    reply: ReplyCreate,
    db: Session = Depends(get_db),
    client: ThreadsClient = Depends(get_threads_client),
    user_id: str = Depends(get_current_user_id)
):
    try:
        media_id = await client.reply(reply.text, reply.parent_media_id, user_id=user_id)
        
        # Save to DB
        db_reply = ReplyModel(
            threads_reply_id=media_id,
            parent_media_id=reply.parent_media_id,
            text=reply.text,
            author=reply.author # Optional context
        )
        db.add(db_reply)
        db.commit()
        db.refresh(db_reply)
        return db_reply
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/{media_id}", response_model=InsightsSchema)
async def get_insights(
    media_id: str,
    db: Session = Depends(get_db),
    client: ThreadsClient = Depends(get_threads_client)
):
    try:
        data = await client.get_insights(media_id)
        # Parse data which usually looks like list of metric objects
        # Mocking parsing logic for standard Graph API response structure:
        # data = [ { "name": "views", "values": [{"value": 123}] }, ... ]
        
        snapshot = InsightsSnapshot(threads_media_id=media_id)
        
        # Simple flattener (assuming standard structure)
        for metric in data:
            if metric.get("name") == "views":
                snapshot.views = metric["values"][0]["value"]
            elif metric.get("name") == "likes":
                snapshot.likes = metric["values"][0]["value"]
            elif metric.get("name") == "replies":
                snapshot.replies = metric["values"][0]["value"]
            elif metric.get("name") == "reposts":
                snapshot.reposts = metric["values"][0]["value"]
            elif metric.get("name") == "quotes":
                snapshot.quotes = metric["values"][0]["value"]
        
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return snapshot
    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
