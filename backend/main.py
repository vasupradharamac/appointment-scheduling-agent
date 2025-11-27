from fastapi import FastAPI
from backend.api.calendly_integration import router as calendly_router

app = FastAPI(
    title="Mock Calendly Scheduling API",
    description="Backend simulation for medical appointment scheduling assessment."
)

app.include_router(calendly_router, prefix="/api/calendly")
