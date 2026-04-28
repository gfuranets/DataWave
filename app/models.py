from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String(50), unique = True, nullable = False)
    password = Column(String(255), nullable = False)

    ship = relationship("Ship", back_populates="user")


class Ship(Base):
    __tablename__ = "ship"

    ship_id = Column(Integer, primary_key = True, autoincrement = True)
    user_id_refer = Column(Integer, ForeignKey("user.user_id"))
    name = Column(String(50), unique = True, nullable = False)

    user = relationship("User", back_populates="ship")
    data = relationship("Data", back_populates="ship")


class Data(Base):    
    __tablename__ = "data"

    data_id = Column(Integer, primary_key = True, autoincrement = True)
    ship_id_refer = Column(Integer, ForeignKey("ship.ship_id"))
    data = Column(String(40))
    timestamp = Column(DateTime)

    ship = relationship("Ship", back_populates="data")
