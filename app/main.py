from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
import models, schemas, crud

app = FastAPI()

@app.get('/users/{user_id}', response_model = schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    # .filter() requires a comparison (==), or use .filter_by()
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user


@app.get('/data/view/', response_model = list[schemas.Data])
async def get_ship_data(start: datetime, end: datetime, db: Session = Depends(get_db)):
    """
    Query ship data by timestamp. 
    Example: /data/view/?start=2023-01-01T00:00:00&end=2023-01-02T00:00:00
    """
    data = crud.view_data(db, t_begin = start, t_end = end)
    return data


@app.post('/users/', response_model = schemas.CreateUser)
async def signup(user: schemas.CreateUser, db: Session = Depends(get_db)):
    return crud.create_user(user, db)

# signup
# login
# change user
# delete user

# add ship
# change ship
# delete ship

# post data
# view data (graph)
