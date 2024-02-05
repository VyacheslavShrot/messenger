from fastapi import APIRouter

messages_router = APIRouter()


@messages_router.get("/")
async def read_root():
    return {"message": "Hello, World!"}
