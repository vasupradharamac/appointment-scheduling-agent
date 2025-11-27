from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    AvailabilityRequest,
    AvailabilityResponse,
    BookingRequest,
    BookingResponse
)
from backend.tools.availability_tool import get_availability
from backend.tools.booking_tool import create_booking

router = APIRouter()

@router.post("/availability", response_model=AvailabilityResponse)
def check_availability(req: AvailabilityRequest):
    try:
        slots = get_availability(req.date, req.appointment_type)
        return {
            "date": req.date,
            "available_slots": slots
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/book", response_model=BookingResponse)
def book_appointment(req: BookingRequest):
    try:
        booking = create_booking(req.dict())
        return booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
