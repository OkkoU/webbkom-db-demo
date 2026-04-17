import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)


def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        # Create the schema
        cur.execute("""
            --- ROOMS
            CREATE TABLE IF NOT EXISTS hotel_rooms (
                id          SERIAL PRIMARY KEY,
                room_number INT NOT NULL UNIQUE,
                type        VARCHAR NOT NULL,
                price       NUMERIC(10,2) NOT NULL DEFAULT 100
            );

            --- GUESTS
            CREATE TABLE IF NOT EXISTS hotel_guests (
                id          SERIAL PRIMARY KEY,
                firstname   VARCHAR NOT NULL,
                lastname    VARCHAR NOT NULL,
                address     VARCHAR DEFAULT NULL,
                email       VARCHAR NOT NULL UNIQUE,
                phone       VARCHAR DEFAULT NULL
            );

            -- BOOKINGS
            CREATE TABLE IF NOT EXISTS hotel_bookings (
                id          SERIAL PRIMARY KEY,
                guest_id    INT NOT NULL REFERENCES hotel_guests(id) ON DELETE CASCADE,
                room_id     INT NOT NULL REFERENCES hotel_rooms(id)  ON DELETE RESTRICT,
                datefrom    DATE NOT NULL,
                dateto      DATE NOT NULL,
                addinfo     VARCHAR DEFAULT NULL,
                created_at  TIMESTAMP DEFAULT now(),
                CHECK       (dateto > datefrom)
            );

        """)
