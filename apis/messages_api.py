import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi import WebSocket
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect

from utils.cache import get_and_save_cache_messages
from utils.chat import create_chat_handler
from utils.logger import logger
from utils.models import UserB, Chat
from utils.mongodb import get_db
from utils.token import get_current_active_user

messages_router = APIRouter()


@messages_router.post("/chat/create")
async def create_chat(user_b: UserB, user_a: str = Depends(get_current_active_user)):
    try:
        users_collection = (await get_db())['users']
        chat_collection = (await get_db())['chat']

        user_a_username = user_a.get("username")
        user_b_username = user_b.username

        result, error = await create_chat_handler(
            users_collection,
            chat_collection,
            user_a_username,
            user_b_username
        )
        if error:
            return {"error": result.get("error")}

        return {
            "success": True,
            "user_a_username": user_a_username,
            "user_b_username": user_b_username,
            "chat_id": result
        }
    except Exception as e:
        logger.error(f"An error occurred while create chat | {e}")


chat_websockets = {}


@messages_router.websocket("/chat/{chat_id}")
async def chat_ws(chat_id: str, websocket: WebSocket):
    try:
        await websocket.accept()

        if chat_id not in chat_websockets:
            chat_websockets[chat_id] = [websocket]
        else:
            chat_websockets[chat_id].append(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                await _send_message_to_chat(chat_id, data)
        except WebSocketDisconnect:
            chat_websockets[chat_id].remove(websocket)
            logger.info("Disconnect WebSocket")
    except Exception as e:
        logger.error(f"An error occurred in chat websocket | {e}")


async def _send_message_to_chat(chat_id: str, message: str):
    try:
        for ws in chat_websockets.get(chat_id, []):
            await ws.send_text(message)
    except Exception as e:
        logger.error(f"An error occurred while sending message to chat {chat_id} | {e}")


@messages_router.post("/send-message")
async def send_message(chat: Chat, user_a: str = Depends(get_current_active_user)):
    try:
        chat_collection = (await get_db())['chat']
        messages_collection = (await get_db())['messages']

        chat_id = chat.chat_id
        message_text = chat.message

        if not message_text:
            return {"error": "Param message is required*"}

        existing_chat = await chat_collection.find_one({"_id": ObjectId(chat_id)})
        if not existing_chat:
            return JSONResponse(status_code=404, content={"error": "There is no such chat with such chat_id"})

        user_a_username = user_a.get("username")
        user_b_username = existing_chat.get("user_b_username")

        send_message_to = user_b_username
        if user_a_username == user_b_username:
            send_message_to = existing_chat.get("user_a_username")

        await messages_collection.insert_one(
            {
                "message": message_text,
                "from": user_a_username,
                "to": send_message_to,
                "chat_id": chat_id,
                "send_in": datetime.datetime.now()
            }
        )

        await get_and_save_cache_messages(
            chat_id,
            message_text,
            user_a_username,
            send_message_to,
            for_send_messages=True
        )

        await _send_message_to_chat(chat_id, message_text)

        return {"success": True, "message": "Message sent successfully"}
    except Exception as e:
        logger.error(f"An error occurred while send message  | {e}")


@messages_router.get("/messages")
async def get_messages(chat: Chat, user_a: str = Depends(get_current_active_user)):
    try:
        chat_id = chat.chat_id

        cached_messages, cache_key, cache = await get_and_save_cache_messages(chat_id, for_get_messages=True)

        if cached_messages is None:
            messages_collection = (await get_db())['messages']
            messages = await messages_collection.find({"chat_id": chat_id}).sort("send_in", -1).to_list(length=None)
            if not messages:
                return {"error": "This chat does not exist or there are no messages in this chat"}

            response = []

            for message in messages:
                response.append(
                    {
                        "from": message.get("from"),
                        "to": message.get("to"),
                        "message": message.get("message"),
                        "send_in": message.get("send_in"),
                    }
                )
            await cache.set(cache_key, response)
        else:
            response = cached_messages

        return {
            "success": True,
            "chat_id": chat_id,
            "messages": response if response is not [] else None
        }
    except Exception as e:
        logger.error(f"An error occurred while get messages | {e}")
