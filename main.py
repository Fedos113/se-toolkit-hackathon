"""
Event Countdown Timer - Main Application
FastAPI backend with static file serving and API endpoints.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os

import database
from scheduler import start_scheduler, stop_scheduler

app = FastAPI(title="Event Countdown Timer", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start background scheduler on startup
@app.on_event("startup")
async def startup_event():
    """Start the background scheduler when the app starts."""
    start_scheduler()

# Stop scheduler on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Stop the background scheduler when the app shuts down."""
    stop_scheduler()

# Serve static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# Pydantic models
class EventCreate(BaseModel):
    title: str
    target_datetime: str  # ISO 8601 format
    user_session_id: str  # Required for user isolation


class EventResponse(BaseModel):
    id: int
    title: str
    target_datetime: str
    created_at: str
    user_session_id: Optional[str]
    notified: bool


# Routes
@app.get("/")
async def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse(os.path.join(static_path, "index.html"))


@app.get("/server-time")
async def get_server_time():
    """Return current server time in UTC."""
    return {"server_time": datetime.utcnow().isoformat()}


@app.get("/events", response_model=list[EventResponse])
async def list_events(user_session_id: str = Query(..., description="User session ID to filter events")):
    """Retrieve all events for a specific user session."""
    try:
        events = database.get_events_by_session_id(user_session_id)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate):
    """Create a new event."""
    try:
        # Validate datetime format
        datetime.fromisoformat(event.target_datetime)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO 8601 (e.g., 2026-04-08T15:30:00)")
    
    if not event.title.strip():
        raise HTTPException(status_code=400, detail="Event title cannot be empty")
    
    try:
        created_event = database.create_event(
            title=event.title.strip(),
            target_datetime=event.target_datetime,
            user_session_id=event.user_session_id
        )
        return created_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/events/{event_id}")
async def delete_event(event_id: int, user_session_id: str = Query(..., description="User session ID for authorization")):
    """Delete an event by ID. Requires user_session_id for authorization."""
    success = database.delete_event_by_session_id(event_id, user_session_id)

    if not success:
        raise HTTPException(status_code=404, detail="Event not found or you don't have permission to delete it")
    return {"message": "Event deleted successfully"}


@app.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int):
    """Get a single event by ID."""
    event = database.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
