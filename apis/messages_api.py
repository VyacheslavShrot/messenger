from fastapi import APIRouter, Depends

from utils.token import get_current_active_user

messages_router = APIRouter()


@messages_router.get("/")
async def read_root(current_user: str = Depends(get_current_active_user)):
    return {"message": "Hello, World!"}
