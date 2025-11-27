import json
from datetime import datetime, timedelta

APPOINTMENT_DURATIONS = {
    "consultation": 30,
    "followup": 15,
    "physical": 45,
    "specialist": 60
}

def load_schedule():
    with open("data/doctor_schedule.json", "r") as f:
        return json.load(f)

def generate_time_slots(start, end, duration_minutes):
    slots = []
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")

    while current + timedelta(minutes=duration_minutes) <= end_time:
        slot_end = current + timedelta(minutes=duration_minutes)
        slots.append((current.strftime("%H:%M"), slot_end.strftime("%H:%M")))
        current += timedelta(minutes=15)
    return slots

def is_conflict(slot_start, slot_end, existing):
    s1 = datetime.strptime(slot_start, "%H:%M")
    e1 = datetime.strptime(slot_end, "%H:%M")

    for appt in existing:
        s2 = datetime.strptime(appt["start"], "%H:%M")
        e2 = datetime.strptime(appt["end"], "%H:%M")
        if not (e1 <= s2 or e2 <= s1):
            return True
    return False

def get_availability(date, appointment_type):
    schedule = load_schedule()
    working_hours = schedule["working_hours"]
    existing = schedule["appointments"].get(date, [])

    duration = APPOINTMENT_DURATIONS[appointment_type]

    all_slots = generate_time_slots(
        working_hours["start"],
        working_hours["end"],
        duration
    )

    results = []
    for start_time, end_time in all_slots:
        results.append({
            "start_time": start_time,
            "end_time": end_time,
            "available": not is_conflict(start_time, end_time, existing)
        })

    return results
