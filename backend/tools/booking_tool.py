import uuid
import random
import string

def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_booking(data: dict):
    booking_id = f"APPT-{uuid.uuid4().hex[:8].upper()}"
    confirmation = generate_confirmation_code()

    return {
        "booking_id": booking_id,
        "status": "confirmed",
        "confirmation_code": confirmation,
        "details": data
    }
