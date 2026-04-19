from pydantic import BaseModel
from datetime import datetime


class CreateUser(BaseModel):
    username: str
    email: str


class ChangeUser(BaseModel):
    username: str | None = None
    email: str | None = None


class CreateShip(BaseModel):
    user_id_refer: int
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
