from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Morjens Dev Okko!", "v": "0.2" }


@app.get("/api/ip")
def ip(request: Request):
    return {"ip":  request.client.host}


@app.get("/ip", response_class=HTMLResponse)
def ip(request: Request):
    return f"<h1>IP-adressen är: {request.client.host}</h1>"
