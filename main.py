from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
app = FastAPI()

bookings = {}


@app.get("/")
async def root():
    return {"status": "API is running"}




@app.get("/availability")
async def check_availability(date: str):
    return {
        "date": date,
        "available": True,
        "slots": ["10:00", "14:00", "16:00"]
    }


class Booking(BaseModel):
    date: str
    time: str


@app.post("/bookings")
async def create_booking(booking: Booking):
    booking_id = f"BK{len(bookings) + 1:03d}"

    bookings[booking_id] = {
        "booking_id": booking_id,
        "date": booking.date,
        "time": booking.time,
        "status": "confirmed"
    }

    return bookings[booking_id]


@app.get("/bookings/{booking_id}")
async def lookup_booking(booking_id: str):
    if booking_id not in bookings:
        return {
            "error": "Booking not found"
        }

    return bookings[booking_id]