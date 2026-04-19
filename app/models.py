from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String(30), unique = True, nullable = False)
    email = Column(String(40), unique = True, nullable = False)


class Ship(Base):
    __tablename__ = "ship"

    ship_id = Column(Integer, primary_key = True, autoincrement = True)
    user_id_refer = Column(Integer, ForeignKey("user.user_id"))
    code = Column(String(10), unique = True)
    name = Column(String(50), unique = True, nullable = False)


class Data(Base):    
    __tablename__ = "data"

    data_id = Column(Integer, primary_key = True, autoincrement = True)
    ship_id_refer = Column(Integer, ForeignKey("ship.ship_id"))
    data = Column(String(40))
    timestamp = Column(DateTime)
