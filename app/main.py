from fastapi import FastAPI, Depends, HTTPException, Request, Form, status, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
import models, crud
from auth import get_current_user, get_current_user_optional, verify_password, create_access_token
from manager import ConnectionManager

app = FastAPI()

templates = Jinja2Templates(directory = "templates")
app.mount("/static", StaticFiles(directory = "static"), name = "static")

# Load main page depending on authentification
@app.get("/", name = "index")
async def index(
    request: Request,
    user: models.User = Depends(get_current_user_optional)
):
    if user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "user": user}
        )

    return templates.TemplateResponse(
        "index_guest.html",
        {"request": request}
    )

# Load 
@app.get("/signup", name = "signup")
async def signup_page(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )


@app.post("/signup", name = "signup")
async def signup(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    exists = db.query(models.User).filter(models.User.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    crud.signup(username, password, db)
    return RedirectResponse("/", status_code=303)


@app.get("/login", name = "login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@app.post("/login", name = "login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": str(user.user_id)})

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response


@app.get("/logout", name = "logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@app.get("/data", name = "data")
async def data_page(
    request: Request,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    data = db.query(models.User).all()
    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "data": data,
            "user": user
        }
    )

# @app.post('/users/patch')
# async def patch(changed_user: schemas.ChangeUser, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.user_id == changed_user.user_id).first()

#     if (changed_user.username != None):
#         user.username = changed_user.username

#     if (changed_user.email != None):
#         user.email = changed_user.email
    
#     db.commit()
#     db.refresh(user)
#     return RedirectResponse("/", status_code = 303)


# @app.post('/user/delete')
# async def delete(user_id: int, db: Session = Depends(get_db)):
#     crud.delete(user_id, db)
#     return RedirectResponse("/", status_code = 303)



@app.get("/ships", name = "ships")
async def ships_page(request: Request,
                     db: Session = Depends(get_db),
                     user: models.User = Depends(get_current_user)):
    
    ships = db.query(models.Ship).filter(models.Ship.user_id_refer == user.user_id).all()
    
    return templates.TemplateResponse("ships.html",
                                      {"request": request,
                                       "ships": ships})
   

@app.post("/ships/create")
async def create_ship(name: Annotated[str, Form()],
                      db: Session = Depends(get_db),
                      user: models.User = Depends(get_current_user)):
    ship = db.query(models.Ship).filter(models.Ship.name == name).first()
    if ship:
        return HTTPException(status_code=400, detail="Ship already exists")
    
    crud.create_ship(user.user_id, name, db)
    return RedirectResponse('/ships', status_code=303)


# @app.post('/ships/patch')
# async def patch_ship(changed_ship: schemas.ChangeShip, db: Session = Depends(get_db)):
#     ship = db.query(models.Ship).filter(models.Ship.ship_id == changed_ship.ship_id).first()

#     if (changed_ship.user_id_refer != None):
#         ship.user_id_refer = changed_ship.user_id_refer
    
#     if (changed_ship.name != None):
#         ship.name = changed_ship.name

#     db.commit()
#     db.refresh(ship)
#     return RedirectResponse("/", status_code = 303)


@app.delete('/ship/delete')
async def delete_ship(ship_id: int, db: Session = Depends(get_db)):
    crud.delete_ship(ship_id, db)
    return RedirectResponse("/ships", status_code = 303)


manager = ConnectionManager()


@app.websocket('/ws')
async def echo(websocket: WebSocket, 
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    await manager.connect(websocket)

    try:
        while True:
            # Control MCUs
            manager.send_command('a', websocket)

            # Process incoming data
            data = manager.receive_data(websocket)
            crud.post_data(1, data, datetime.now(), db)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

# add ship Y
# change ship Y 
# delete ship Y 

# post data ws
# view data (graph)
