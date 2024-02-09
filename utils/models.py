from pydantic import BaseModel, constr


class User(BaseModel):
    username: constr(min_length=6, max_length=16)
    password: constr(min_length=8, max_length=16)


class UserB(BaseModel):
    username: constr(min_length=6, max_length=16)
