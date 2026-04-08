# Implementation Plan - Event Countdown Timer

## Version 1: Core MVP (Barebones)

**Goal:** Deliver a minimal but fully working countdown timer that works locally. Focus on the absolute minimum to demonstrate the concept.

### Core Feature
**Real-time countdown display** - Users can add events and watch live countdowns. No notifications, no sharing—just the core ticking timer.

### Architecture

| Component | Technology | Role |
|-----------|------------|------|
| **Backend** | Python + FastAPI | Simple REST API for CRUD operations |
| **Database** | SQLite (file-based, no pooling) | Stores `event_id`, `title`, `target_datetime`, `created_at` |
| **Client** | Vanilla HTML/CSS/JS Web App | Basic dashboard to add/view events with live countdown rendering |

### Implementation Steps

#### 1. Project Scaffold
- [x] Initialize FastAPI backend structure
- [x] Set up SQLite database with basic schema
- [x] Create static frontend folder structure (`static/`)
- [x] Configure CORS and static file serving in FastAPI
- [x] Create `requirements.txt` with minimal dependencies: `fastapi`, `uvicorn`

#### 2. Database Setup
- [x] Design minimal schema: `events` table with columns:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `title` (TEXT NOT NULL)
  - `target_datetime` (TEXT NOT NULL, ISO 8601)
  - `created_at` (TEXT NOT NULL, default CURRENT_TIMESTAMP)
- [x] Implement basic database initialization

#### 3. API Endpoints
- [x] `GET /events` - Retrieve all events
- [x] `POST /events` - Create a new event (basic validation only)
- [x] `DELETE /events/{event_id}` - Delete an event by ID
- [x] Add basic error handling (no advanced status codes)

#### 4. Frontend UI
- [x] Create simple, functional dashboard layout
- [x] Build input form:
  - Event title text input
  - Date/time picker
  - "Add Event" button (basic validation)
- [x] Build event list display:
  - Event title and target date
  - Live countdown timer (days, hours, minutes, seconds)
  - Delete button
- [x] Implement `setInterval` for countdown updates (client-side time sync only)

### V1 Deliverable
✅ Localhost web app where users can add events and watch live countdowns. No notifications, no sharing—core functionality only.

---

## Version 2: Notifications & Polish

**Goal:** Add the high-value notification system, improve reliability, and enhance UX based on V1 testing.

### Enhancements Over V1

| Component | Addition | Role |
|-----------|----------|------|
| **Backend** | APScheduler integration | Background scanning for notification triggers |
| **Client** | Browser Notification API | Desktop push notifications when events start |
| **Database** | Add `notified` flag + `user_session_id` | Track notification state and prepare for future auth |
| **Security** | User session isolation | Each user only sees and manages their own events via session-based filtering |

### Implementation Steps

#### 1. Notification System
- [x] Request Notification permission on first page load
- [x] Implement client-side notification trigger when countdown hits `00:00:00`
- [x] Design notification payload: event title + "has started!" message
- [x] Test notification behavior across Chrome, Firefox, Edge

#### 2. Background Scheduler
- [x] Integrate APScheduler to scan database every 30 seconds
- [x] Identify events where `target_datetime <= now` and `notified == false`
- [x] Mark events as `notified = true` to prevent duplicate alerts
- [x] Handle edge cases: missed events during downtime, server restarts

#### 3. Database Enhancements
- [x] Add columns to existing schema:
  - `user_session_id` (TEXT, nullable)
  - `notified` (BOOLEAN DEFAULT 0)
- [x] Update CRUD operations to handle new fields

#### 4. Frontend Improvements
- [x] Add visual state changes as event approaches (color shifts)
- [x] Sync countdown to server time (`GET /server-time` endpoint)
- [x] Add responsive CSS for mobile/desktop compatibility
- [x] Improve input validation with user feedback

#### 5. Testing & Demo Prep
- [x] Test event creation, persistence across page refreshes
- [x] Verify timezone handling (all times stored in UTC)
- [x] Test notification delivery accuracy
- [x] Prepare 3-minute live demo script for TA:
  1. Add an event 3 minutes in the future
  2. Show countdown ticking down
  3. Wait for notification to fire at exactly 00:00:00
  4. Demonstrate event deletion and page refresh persistence

#### 6. User Session Isolation
- [x] Implement session-based event filtering in database layer
- [x] Update API endpoints to accept `user_session_id` query parameter
- [x] Frontend automatically sends session ID with all requests
- [x] Users can only view and delete their own events
- [x] Session ID stored in localStorage for persistence across page reloads

### V2 Deliverable
✅ Fully functional localhost web app with live countdowns, desktop notifications, reliable background scheduling, and user session isolation. Ready for TA demo.

---

## TA Feedback Log

> **Instructions:** Record all feedback received from TA during V1 demo session. Apply feedback before V2 final submission.

| # | Date | Feedback From | Feedback Item | Status | Applied In |
|---|------|---------------|---------------|--------|------------|
| - | - | - | _Awaiting V1 demo feedback_ | ⏳ Pending | - |

### Feedback Applied During V2 Development
- _None yet — awaiting V1 demo session feedback_