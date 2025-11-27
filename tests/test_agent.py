from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_availability():
    res = client.post("/api/calendly/availability", json={
        "date": "2024-01-15",
        "appointment_type": "consultation"
    })
    assert res.status_code == 200
    assert "available_slots" in res.json()

def test_booking():
    res = client.post("/api/calendly/book", json={
        "appointment_type": "consultation",
        "date": "2024-01-15",
        "start_time": "10:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-555-0100"
        },
        "reason": "Annual checkup"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "confirmed"
