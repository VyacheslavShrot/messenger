from fastapi import APIRouter, Depends

from utils.chat import create_chat_handler
from utils.logger import logger
from utils.models import UserB
from utils.mongodb import get_db
from utils.token import get_current_active_user

messages_router = APIRouter()


@messages_router.post("/chat/create")
async def create_chat(user_b: UserB, user_a: str = Depends(get_current_active_user)):
    try:
        users_collection = (await get_db())['users']
        messages_collection = (await get_db())['messages']

        user_a_username = user_a.get("username")
        user_b_username = user_b.username

        result = await create_chat_handler(
            users_collection,
            messages_collection,
            user_a_username,
            user_b_username
        )

        return {
            "success": True,
            "user_a_username": user_a_username,
            "user_b_username": user_b_username,
            "chat_id": result
        }
    except Exception as e:
        logger.error(f"An error occurred while create chat | {e}")
