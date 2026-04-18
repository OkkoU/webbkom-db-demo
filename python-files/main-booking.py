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

# Skapa databas-schema
create_schema()


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



# ── Schema ──────────────────────────────────────────────────── Datamodell för bokning
class Booking(BaseModel):
    guest_id: int
    room_id:  int



# ── Rooms ─────────────────────────────────────────────────────
@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                room_number AS number,
                type,
                price
            FROM hotel_rooms
            ORDER BY room_number
        """)

        rooms = cur.fetchall()

    return rooms



# ── Bookings ──────────────────────────────────────────────────
@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT
                b.id,
                b.datefrom    AS date,
                b.dateto,
                b.addinfo     AS notes,
                r.room_number AS room_name,
                b.created_at
            FROM hotel_bookings b
            JOIN hotel_rooms r ON r.id = b.room_id
            ORDER BY b.datefrom DESC
        """)

        return cur.fetchall()


@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (
                guest_id,
                room_id
            )
            VALUES (
                %s, %s
            )
        """, (
            booking.guest_id,
            booking.room_id
        ))

    return {"msg": "Booking created!"}
