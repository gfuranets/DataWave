from sqlalchemy.orm import Session
import models, schemas
import datetime

def signup(user: schemas.CreateUser, db: Session):
    db_user = models.User(username = user.username,
                          email = user.email)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def login():
    pass


def delete_user(user_id: int, db: Session):
    db_user = db.query(models.User).filter(user_id == user_id).first()

    db.delete(db_user)
    db.commit()


def create_ship(user_id: int, ship: schemas.CreateShip, db: Session):
    db_ship = models.Ship(user_id_refer = user_id,
                          code = f"S-{user_id}",
                          name = ship.name)
    
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)


def change_ship(ship_id: int, ship: schemas.ChangeShip, db: Session):
    pass


def delete_ship(ship_id: int, db: Session):
    db_ship = db.query(models.Ship).filter(ship_id == ship_id).first()

    db.delete(db_ship)
    db.commit()


def post_data(ship_id_refer: int, data: str, timestamp: datetime.datetime, db: Session):
    db_data = models.Data(ship_id_refer = data.ship_id_refer,
                          data = data,
                          timestamp = timestamp)
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
