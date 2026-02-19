from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory = "templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})

@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html",
                                      {"request": request})

@app.get("/data")
def data(request: Request):
    return templates.TemplateResponse("data.html",
                                      {"request": request})

@app.get("/map")
def data(request: Request):
    return templates.TemplateResponse("map.html",
                                      {"request": request})