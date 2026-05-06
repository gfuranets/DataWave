import asyncio
from fastapi import FastAPI, Depends, HTTPException, Request, Form, WebSocket, WebSocketDisconnect
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
from ws_auth import get_user_from_token

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

manager = ConnectionManager()


@app.get("/")
async def index(request: Request, 
                user: models.User = Depends(get_current_user_optional)):
    if user:
        return templates.TemplateResponse("index.html", {"request": request, "user": user})
    return templates.TemplateResponse("index_guest.html", {"request": request})


@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
async def signup(username: str = Form(), 
                 password: str = Form(), 
                 db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(400, "Username exists")

    crud.signup(username, password, db)
    return RedirectResponse("/", status_code=303)


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(401, "Wrong credentials")

    token = create_access_token({"sub": str(user.user_id)})

    response = RedirectResponse("/", status_code=303)
    response.set_cookie("access_token", token, httponly=True)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@app.get("/ships")
async def ships_page(request: Request, 
                     db: Session = Depends(get_db), 
                     user: models.User = Depends(get_current_user)):
    ships = db.query(models.Ship).filter(models.Ship.user_id_refer == user.user_id).all()
    return templates.TemplateResponse("ships.html", {"request": request, "ships": ships})


@app.post("/ships/create")
async def create_ship(name: str = Form(), 
                      db: Session = Depends(get_db), 
                      user: models.User = Depends(get_current_user)):
    crud.create_ship(user.user_id, name, db)
    return RedirectResponse("/ships", status_code=303)


@app.get("/chart/{ship_id}")
async def chart_page(request: Request, 
                     ship_id: int,
                     db: Session = Depends(get_db),
                     user: models.User = Depends(get_current_user)):
    raw_data = db.query(models.Data).filter(models.Data.ship_id_refer == ship_id).all()
    parsed_data = []
    for d in raw_data:
        parts = d.data.split(",")
        if len(parts) >= 6:
            parsed_data.append({
                "time": d.timestamp.isoformat(),
                "temperature": float(parts[0]),
                "pressure": float(parts[1]),
                "humidity": float(parts[2]),
                "mag_x": float(parts[3]),
                "mag_y": float(parts[4]),
                "mag_z": float(parts[5])
            })
            
    return templates.TemplateResponse("chart.html", {"request": request, 
                                                     "ship_id": ship_id,
                                                     "data": parsed_data})


@app.get("/api/data/{ship_id}")
async def get_data(ship_id: int, 
                   db: Session = Depends(get_db)):
    data = db.query(models.Data).filter(models.Data.ship_id_refer == ship_id).all()
    return [{"value": d.data, "time": d.timestamp} for d in data]


# ESP32 data WebSocket
@app.websocket("/ws/{ship_id}")
async def websocket_ship(websocket: WebSocket,
                         ship_id: int,
                         token: str,
                         db: Session = Depends(get_db)):
    print(f"[WS] Connection attempt: ship_id={ship_id}, token={token[:8]}...")

    ship = db.query(models.Ship).filter(
        models.Ship.ship_id == ship_id,
        models.Ship.token == token
    ).first()
    if not ship:
        print(f"[WS] Rejected: ship not found or token mismatch")
        await websocket.close()
        return

    print(f"[WS] Ship {ship_id} authenticated, accepting connection")
    await manager.connect(ship_id, websocket)
    queue = manager.cmd_queues[ship_id]

    async def pump_commands():
        try:
            while True:
                cmd = await queue.get()
                await websocket.send_text(cmd)
        except Exception:
            pass

    cmd_task = asyncio.create_task(pump_commands())

    try:
        while True:
            data = await websocket.receive_text()
            print(f"[WS] Ship {ship_id} data: {data[:60]}")

            if not data[0].isdigit() and not data[0] == '-':
                print(f"[WS] Skipping non-sensor message: {data[:30]}")
                continue

            crud.post_data(ship_id, data, datetime.now(), db)

    except WebSocketDisconnect:
        print(f"[WS] Ship {ship_id} disconnected")
    except Exception as e:
        print(f"[WS] Error for ship {ship_id}: {e}")
    finally:
        cmd_task.cancel()
        manager.disconnect(ship_id)


# Browser control WebSocket (for servo commands)
@app.websocket("/ws-control/{ship_id}")
async def websocket_control(websocket: WebSocket,
                            ship_id: int,
                            db: Session = Depends(get_db)):
    # Authenticate from cookie
    token = websocket.cookies.get("access_token")
    if not token:
        print(f"[CTRL] Rejected: no auth cookie")
        await websocket.close()
        return

    user = get_user_from_token(token, db)
    if not user:
        print(f"[CTRL] Rejected: invalid token")
        await websocket.close()
        return

    # Verify user owns this ship
    ship = db.query(models.Ship).filter(
        models.Ship.ship_id == ship_id,
        models.Ship.user_id_refer == user.user_id
    ).first()
    if not ship:
        print(f"[CTRL] Rejected: user doesn't own ship {ship_id}")
        await websocket.close()
        return

    print(f"[CTRL] User {user.user_id} controlling ship {ship_id}")
    await websocket.accept()

    try:
        while True:
            command = await websocket.receive_text()
            sent = await manager.send_command(ship_id, command)
            if not sent:
                await websocket.send_text("ERR:ESP32_NOT_CONNECTED")
    except WebSocketDisconnect:
        print(f"[CTRL] User disconnected from ship {ship_id}")
        