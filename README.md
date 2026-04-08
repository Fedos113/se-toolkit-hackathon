# Event Countdown Timer

A real-time event countdown timer with desktop notifications, built with FastAPI and vanilla JavaScript.

## Product Definition

| Item | Description |
|------|-------------|
| **End-User** | Students, professionals, anyone who tracks deadlines and events |
| **Problem** | People miss important events because they forget to check calendars or don't get timely reminders |
| **One-Liner** | "A web page where you add events, watch live countdowns, and get desktop notifications when they arrive" |
| **Core Feature** | Real-time live countdown display (days/hours/minutes/seconds) with automatic desktop notifications |

## Features

### Version 1 - Core MVP
- ✅ Add events with title and target date/time
- ✅ Real-time countdown display (days, hours, minutes, seconds)
- ✅ Delete events
- ✅ Persistent storage with SQLite
- ✅ Clean, responsive UI

### Version 2 - Notifications & Polish
- ✅ Desktop push notifications when events start
- ✅ Background scheduler for reliable notification delivery
- ✅ Visual state changes as events approach (color shifts)
- ✅ Server-client time synchronization
- ✅ Responsive design for mobile/desktop
- ✅ Notification state tracking in database

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python + FastAPI |
| Database | SQLite |
| Scheduler | APScheduler |
| Frontend | Vanilla HTML/CSS/JS |

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to customize host, port, or database path.

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The app will be available at: **http://localhost:8000**

## Usage

1. Open http://localhost:8000 in your browser
2. (Optional) Click "Enable Desktop Notifications" to allow browser notifications
3. Add an event:
   - Enter an event title
   - Select a future date and time
   - Click "Add Event"
4. Watch the live countdown timer
5. Get notified when the event starts!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve the main page |
| GET | `/server-time` | Get current server time (UTC) |
| GET | `/events` | List all events |
| POST | `/events` | Create a new event |
| GET | `/events/{id}` | Get event by ID |
| DELETE | `/events/{id}` | Delete an event |

### Request/Response Examples

**Create Event:**
```json
POST /events
{
  "title": "Product Launch",
  "target_datetime": "2026-04-08T15:30:00"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Product Launch",
  "target_datetime": "2026-04-08T15:30:00",
  "created_at": "2026-04-08T10:00:00",
  "user_session_id": "session_abc123",
  "notified": false
}
```

## Demo Script (3 minutes)

1. Start the application and open http://localhost:8000
2. Enable desktop notifications when prompted
3. Add an event 3 minutes in the future
4. Show the countdown timer ticking down
5. Wait for the notification to fire at exactly 00:00:00
6. Demonstrate event deletion and page refresh persistence

## Project Structure

```
se-toolkit-hackathon/
├── main.py              # FastAPI application and routes
├── database.py          # SQLite database operations
├── scheduler.py         # APScheduler background tasks
├── requirements.txt     # Python dependencies
├── events.db           # SQLite database (auto-created)
├── static/
│   ├── index.html      # Main HTML page
│   ├── style.css       # Styles
│   └── app.js          # Frontend JavaScript
├── .env.example        # Environment template
└── README.md           # This file
```

## License

MIT License - see LICENSE file for details.
