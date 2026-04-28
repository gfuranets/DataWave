from pydantic import BaseModel
from datetime import datetime

class CreateUser(BaseModel):
    username: str
    password: str


class ChangeUser(BaseModel):
    username: str | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateShip(BaseModel):
    # user_id_refer found from token
    name: str

class ChangeShip(BaseModel):
    user_id_refer: int | None = None
    name: str | None = None


class Data(BaseModel):
    ship_id_refer: int
    data: str
    timestamp: datetime

    class Config:
        from_attributes = True
