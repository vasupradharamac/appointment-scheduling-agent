# Medical Appointment Scheduling API – Mock Calendly Integration

This project implements **Core Feature 1: Calendly Integration** from the Lyzr Assessment. It simulates a Calendly-style backend for scheduling medical appointments using realistic slot generation, conflict detection, and booking confirmation logic.

The backend uses **FastAPI** and is intentionally lightweight and modular, making it easy to extend into a full conversational agent if needed.

---------

# Overview

This backend provides two essential capabilities:

1. **Checking appointment availability**
2. **Booking appointments**

It uses mock data with:

- Defined **working hours**
- A list of **previously booked appointments**
- Multiple **appointment types** with different durations
- A **15-minute stepping interval**
- Overlap-based slot availability detection

Everything is stored in JSON for simplicity.

---------

# Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **pytest** (for tests)

-----------

# Appointment Types & Durations

| Appointment Type        | Key           | Duration |
|-------------------------|---------------|----------|
| General Consultation    | consultation  | 30 mins  |
| Follow-up               | followup      | 15 mins  |
| Physical Exam           | physical      | 45 mins  |
| Specialist Consultation | specialist    | 60 mins  |

These durations directly influence the slot sizes during availability computation.

--------

# Availability Logic (How It Works)

## 1. Working Hours
Defined in `data/doctor_schedule.json`:

```json
"working_hours": {
  "start": "09:00",
  "end": "17:00"
}
```
---------

## 2. Slot Generation

For each date:

Determine appointment duration

Move forward in 15-minute steps

Create sliding windows of that duration
Example: For a 30-minute appointment

09:00–09:30

09:15–09:45

09:30–10:00

## 3. Conflict Detection

A generated slot is unavailable if it overlaps with any existing appointment.

Example booked data:

```json
"2024-01-15": [
  { "start": "09:30", "end": "10:00" },
  { "start": "11:00", "end": "11:30" }
]
```
If a generated slot overlaps with these, "available": false.

----------

## 4. Example Availability Response

```json
{
  "date": "2024-01-15",
  "available_slots": [
    { "start_time": "09:00", "end_time": "09:30", "available": true },
    { "start_time": "09:30", "end_time": "10:00", "available": false }
  ]
}
```
# Booking Logic
## 1. Required Inputs

appointment_type

date

start_time

patient (name, email, phone)

reason for visit

## 2. Auto-generated fields

booking_id

Format: APPT-XXXXXXXX

confirmation_code

6-character uppercase alphanumeric

## 3. Example Booking Request

```json
{
  "appointment_type": "consultation",
  "date": "2024-01-15",
  "start_time": "10:00",
  "patient": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0100"
  },
  "reason": "Annual checkup"
}
```
## 4. Example Booking Response

```json
{
  "booking_id": "APPT-72B91A5F",
  "status": "confirmed",
  "confirmation_code": "VCM821",
  "details": {
    "appointment_type": "consultation",
    "date": "2024-01-15",
    "start_time": "10:00",
    "patient": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0100"
    },
    "reason": "Annual checkup"
  }
}
```
------------

# Architecture Diagram

The diagram below represents the module-level architecture.

```
                   ┌────────────────────────────┐
                   │        FastAPI Backend      │
                   │            main.py          │
                   └──────────────┬─────────────┘
                                  │
                        /api/calendly/*
                                  │
         ┌────────────────────────┼──────────────────────────┐
         │                                                │
┌──────────────────────┐                         ┌──────────────────────┐
│ Availability Tool    │                         │ Booking Tool         │
│ get_availability()   │                         │ create_booking()     │
│ conflict detection   │                         │ generate IDs         │
└──────────────────────┘                         └──────────────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ doctor_schedule.json    │
         └────────────────────────┘
```

-------------

## Running the Project

1. Install dependencies

pip install -r requirements.txt

2. Run FastAPI server

uvicorn backend.main:app --reload

-------------

# API Endpoints

## POST /api/calendly/availability

```json
{
  "date": "2024-01-15",
  "appointment_type": "consultation"
}
```

## POST /api/calendly/book

```json
{
  "appointment_type": "consultation",
  "date": "2024-01-15",
  "start_time": "10:00",
  "patient": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0100"
  },
  "reason": "Annual checkup"
}
```
-------------

# Testing

## Run:

```
pytest tests/test_agent.py
```

Best Regards,

Vasupradha R
