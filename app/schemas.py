from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    email: str


class CreateUser(BaseModel):
    username: str
    email: str


class ChangeUser(BaseModel):
    username: str | None = None
    email: str | None = None


class Data(BaseModel):
    data_id: int
    ship_id_refer: int
    region_id_refer: int
    data: str
    timestamp: datetime

    class Config:
        orm_mode = True

