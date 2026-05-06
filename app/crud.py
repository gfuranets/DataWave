from sqlalchemy.orm import Session
import models, schemas
import datetime
import secrets
from auth import hash_password

def signup(username: str, password: str, db: Session):
    db_user = models.User(username = username,
                          password = hash_password(password))
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def delete_user(user_id: int, db: Session):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        
    return db_user


def create_ship(user_id: int, name: str, db: Session):
    token = secrets.token_hex(32)

    db_ship = models.Ship(
        user_id_refer=user_id,
        name=name,
        token=token
    )

    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)

    return db_ship


def delete_ship(ship_id: int, db: Session):
    db_ship = db.query(models.Ship).filter(models.Ship.ship_id == ship_id).first()

    if db_ship:
        db.delete(db_ship)
        db.commit()


def post_data(ship_id_refer: int, data: str, timestamp: datetime, db: Session):
    db_data = models.Data(ship_id_refer = ship_id_refer,
                          data = data,
                          timestamp = timestamp)
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
