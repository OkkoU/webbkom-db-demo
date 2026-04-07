from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return { "msg": "Morjens Dev Okko!", "v": "0.2" }


@app.get("/api/ip")
def ip(request: Request):
    return {"ip":  request.client.host}


@app.get("/ip", response_class=HTMLResponse)
def ip(request: Request):
    return f"<h1>IP-adressen är: {request.client.host}</h1>"


# Hotel Rooms
rooms = [
    {
        "room_number": 101,
        "type": "Single",
        "price": 80
    },
    {
        "room_number": 202,
        "type": "Double",
        "price": 120
    },
    {
        "room_number": 303,
        "type": "Suite",
        "price": 250
    }
]

@app.get("/rooms")
def get_rooms():
    return rooms
