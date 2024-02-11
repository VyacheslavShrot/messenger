from typing import Optional

from pydantic import BaseModel, constr


class User(BaseModel):
    username: constr(min_length=6, max_length=16)
    password: constr(min_length=8, max_length=16)


class UserB(BaseModel):
    username: constr(min_length=6, max_length=16)


class Chat(BaseModel):
    chat_id: str
    message: Optional[str] = None
