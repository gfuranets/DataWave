from sqlalchemy.orm import Session
import models, schemas
import datetime

def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(user: schemas.CreateUser, db: Session):
    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def post_data(data: schemas.Data, db: Session):
    # Fixed: timestap -> timestamp
    # Fixed: ship_id_refer was being used for region_id_refer
    db_data = models.ShipData(
        ship_id_refer = data.ship_id_refer,
        region_id_refer = data.region_id_refer,
        data = data.data,
        timestamp = data.timestamp
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def view_data(db: Session, t_begin: datetime.datetime, t_end: datetime.datetime):
    """Retrieves ship data within a specific time range."""
    return db.query(models.ShipData).filter(
        models.ShipData.timestamp >= t_begin,
        models.ShipData.timestamp <= t_end
    ).all()
