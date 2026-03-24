from sqlalchemy.orm import Session
import models, schemas

def create_sensor_data(db: Session, data: schemas.SensorDataCreate):
    db_data = models.SensorData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_all_sensor_data(db: Session):
    return db.query(models.SensorData).all()
