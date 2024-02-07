from datetime import timedelta

import bcrypt
from fastapi import APIRouter

from utils.logger import logger
from utils.models import User
from utils.mongodb import get_db
from utils.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

users_router = APIRouter()


@users_router.post("/user/register")
async def user_register(user: User):
    try:
        users_collection = (await get_db())['users']

        username = user.username

        if not username.isalnum():
            return {"error": "Username must contain only alphanumeric characters"}

        existing_user = await users_collection.find_one({"username": username})
        if existing_user is not None:
            return {"error": "There's already a user with that nickname"}

        password = user.password

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password = password_hash.decode('utf-8')

        result = await users_collection.insert_one(
            {
                "username": username,
                "password": password
            }
        )

        return {"success": True, "user_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"An error occurred while get user | {e}")


@users_router.post("/user/login")
async def login(user: User):
    try:
        users_collection = (await get_db())['users']

        username = user.username

        existing_user = await users_collection.find_one({"username": username})
        if not existing_user:
            return {"error": "There is no such user with such username"}

        password = user.password
        hashed_password = existing_user.get('password')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            token_data = {"sub": username}

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = await create_access_token(token_data, access_token_expires)

            return {
                "success": True,
                "user_id": str(existing_user.get('_id')),
                "username": existing_user.get("username"),
                "access_token": access_token
            }
        else:
            return {"error": "Invalid password"}
    except Exception as e:
        logger.error(f"An error occurred while get user | {e}")
