from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
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


# Skapa databas-schema
create_schema()


# Datamodell för bokning
class Booking(BaseModel):
    guest_id: int
    room_id:  int
    datefrom: date
    dateto: date
    addinfo: str | None = None


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



# --- Hotel Rooms --------------------
@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                room_number,
                type,
                price
            FROM hotel_rooms
            ORDER BY room_number
        """)

        rooms = cur.fetchall()

    return rooms



# --- Get one Room --------------------
@app.get("/rooms/{id}")
def get_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM hotel_rooms
            WHERE id = %s
        """, [id])

        room = cur.fetchone()

    return room



# --- Bookings --------------------
@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (
                guest_id,
                room_id,
                datefrom,
                dateto,
                addinfo
            )
            VALUES (
                %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            booking.guest_id,
            booking.room_id,
            booking.datefrom,
            booking.dateto,
            booking.addinfo
        ))

        new_booking = cur.fetchone()

    return {"msg": "Booking created!", "id": new_booking['id']}


@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                b.id,
                b.datefrom,
                b.dateto,
                b.addinfo,
                r.room_number
            FROM hotel_bookings b
            JOIN hotel_rooms r ON b.room_id = r.id
            ORDER BY b.datefrom
        """)

        bookings = cur.fetchall()

    return bookings
