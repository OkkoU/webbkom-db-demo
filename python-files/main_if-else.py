from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.db import get_conn, create_schema

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
    # Testa databasen
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                'Databasen funkar!' AS msg,
                version() as version
        """)

        db_status = cur.fetchone()

    return { "msg": "Hotel-API", "db": db_status }



@app.get("/if/{term}")
def if_test(term: str):
    ret_str = "Default message..."
    if term == "hello":
        ret_str = "Hello yourself!"
    elif term == "hej":
        ret_str = "Hej på dig"
    else:
        ret_str = "What do you want?"
    return {"msg": ret_str}
