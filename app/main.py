from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get('/')
def index():
    return "main page"

@app.get('/statistics')
def statistics(db: Session):
    query = crud.get_all_sensor_data(db)
