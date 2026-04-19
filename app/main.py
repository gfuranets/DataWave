from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
import models, schemas, crud
from manager import ConnectionManager

app = FastAPI()

templates = Jinja2Templates(directory = "templates")
app.mount("/static", StaticFiles(directory = "static"), name = "static")

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})

@app.post('/user/signup')
async def signup(user: schemas.CreateUser, db: Session = Depends(get_db)):
    crud.signup(user, db)
    return RedirectResponse("/", status_code = 303)


@app.patch('/users/patch')
async def patch(changed_user: schemas.ChangeUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == changed_user.user_id).first()

    if (changed_user.username != None):
        user.username = changed_user.username

    if (changed_user.email != None):
        user.email = changed_user.email
    
    db.commit()
    db.refresh(user)
    return RedirectResponse("/", status_code = 303)


@app.delete('/user/delete')
async def delete(user_id: int, db: Session = Depends(get_db)):
    crud.delete(user_id, db)
    return RedirectResponse("/", status_code = 303)


@app.post('/ships/create')
async def create_ship(user_id: int, ship: schemas.CreateShip, db: Session = Depends(get_db)):
    crud.create_ship(user_id, ship, db)
    return RedirectResponse("/", status_code = 303)


@app.patch('/ships/patch')
async def patch_ship(changed_ship: schemas.ChangeShip, db: Session = Depends(get_db)):
    ship = db.query(models.Ship).filter(models.Ship.ship_id == changed_ship.ship_id).first()

    if (changed_ship.user_id_refer != None):
        ship.user_id_refer = changed_ship.user_id_refer
    
    if (changed_ship.name != None):
        ship.name = changed_ship.name

    db.commit()
    db.refresh(ship)
    return RedirectResponse("/", status_code = 303)


@app.delete('/ship/delete')
async def delete_ship(ship_id: int, db: Session = Depends(get_db)):
    crud.delete_ship(ship_id, db)
    return RedirectResponse("/", status_code = 303)


manager = ConnectionManager()

# @app.websocket('/wss')
# async def echo(websocket: WebSocket, db: Session = Depends(get_db)):
#     await manager.connect(websocket)

#     try:
#         while True:
#             # Control MCUs
#             manager.send_command('a', websocket)

#             # Process incoming data
#             ship_id_refer, data = manager.receive_data(websocket)

#             crud.post_data(ship_id_refer, data, datetime.datetime.now(), db)



#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

@app.get('/data', name = "data")
async def data(request: Request, db: Session = Depends(get_db)):
    data = db.query(models.User).all()
    return templates.TemplateResponse("data.html",
                                      {"request": request,
                                       "data": data})

# signup Y
# login
# change user Y
# delete user Y

# add ship Y
# change ship Y 
# delete ship Y 

# post data ws
# view data (graph)
