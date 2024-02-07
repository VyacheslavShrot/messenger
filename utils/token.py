import os
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError

from utils.logger import logger
from utils.mongodb import get_db

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def _get_current_user(request: Request):
    try:
        token = request.headers["Authorization"].split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except KeyError:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_active_user(current_user: str = Depends(_get_current_user)):
    try:
        users_collection = (await get_db())['users']

        user = await users_collection.find_one({"username": current_user})

        return user
    except Exception as e:
        logger.error(f"An error occurred while get current user | {e}")
