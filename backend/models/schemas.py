from pydantic import BaseModel
from typing import List

class AvailabilityRequest(BaseModel):
    date: str
    appointment_type: str

class TimeSlot(BaseModel):
    start_time: str
    end_time: str
    available: bool

class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[TimeSlot]

class Patient(BaseModel):
    name: str
    email: str
    phone: str

class BookingRequest(BaseModel):
    appointment_type: str
    date: str
    start_time: str
    patient: Patient
    reason: str

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict
