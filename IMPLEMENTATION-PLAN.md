# Implementation Plan - Event Countdown Timer

## Version 1: Core MVP

**Goal:** Deliver a fully functioning, single-core-feature product that reliably creates countdowns and notifies users. One core thing done well.

### Core Feature
**Real-time countdown display with browser push notifications** - Users can add important dates, watch live countdowns ticking down, and receive desktop notifications the moment an event starts.

### Architecture

| Component | Technology | Role |
|-----------|------------|------|
| **Backend** | Python + FastAPI + APScheduler | REST API for CRUD operations, time synchronization, and background notification triggering |
| **Database** | SQLite | Stores `event_id`, `title`, `target_datetime`, `created_at`, `user_session_id` |
| **Client** | Vanilla HTML/CSS/JS Web App | Dashboard to add/view events, live countdown rendering, and Browser Notification API integration |

### Implementation Steps

#### 1. Project Scaffold
- [ ] Initialize FastAPI backend structure
- [ ] Set up SQLite database with SQLAlchemy or raw SQLite
- [ ] Create static frontend folder structure (`static/`, `templates/`)
- [ ] Configure CORS and static file serving in FastAPI
- [ ] Create `requirements.txt` with dependencies: `fastapi`, `uvicorn`, `apscheduler`, `aiosqlite`

#### 2. Database Setup
- [ ] Design schema: `events` table with columns:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `title` (TEXT NOT NULL)
  - `target_datetime` (TEXT NOT NULL, ISO 8601 UTC)
  - `created_at` (TEXT NOT NULL, default CURRENT_TIMESTAMP)
  - `user_session_id` (TEXT, optional for future auth)
  - `notified` (BOOLEAN DEFAULT 0)
- [ ] Implement database initialization and connection pooling
- [ ] Create database helper functions for CRUD operations

#### 3. API Endpoints
- [ ] `GET /events` - Retrieve all events with their current countdown status
- [ ] `POST /events` - Create a new event with JSON validation
  - Validate `title` (non-empty, max 200 chars)
  - Validate `target_datetime` (future date, ISO 8601 format)
  - Return created event with `event_id`
- [ ] `DELETE /events/{event_id}` - Delete an event by ID
- [ ] `GET /server-time` - Return current server UTC time for client sync
- [ ] Add proper error handling and HTTP status codes

#### 4. Frontend UI
- [ ] Create clean, modern dashboard layout
- [ ] Build input form:
  - Event title text input
  - Date/time picker
  - "Add Event" button with validation feedback
- [ ] Build event cards display:
  - Event title and target date
  - Live countdown timer (days, hours, minutes, seconds)
  - Delete button
  - Visual state changes as event approaches (color shifts)
- [ ] Implement `setInterval` for countdown updates synced to server time
- [ ] Add responsive CSS for mobile/desktop compatibility

#### 5. Notification System
- [ ] Request Notification permission on first page load
- [ ] Implement client-side notification trigger when countdown hits `00:00:00`
- [ ] Design notification payload: event title + "has started!" message
- [ ] Test notification behavior across Chrome, Firefox, Edge

#### 6. Background Scheduler
- [ ] Integrate APScheduler to scan database every 30 seconds
- [ ] Identify events where `target_datetime <= now` and `notified == false`
- [ ] Mark events as `notified = true` to prevent duplicate alerts
- [ ] Handle edge cases: missed events during downtime, server restarts

#### 7. Testing & Demo Prep
- [ ] Test event creation, persistence across page refreshes
- [ ] Verify timezone handling (all times stored in UTC)
- [ ] Test notification delivery accuracy
- [ ] Prepare 3-minute live demo script for TA:
  1. Add an event 3 minutes in the future
  2. Show countdown ticking down
  3. Wait for notification to fire at exactly 00:00:00
  4. Demonstrate event deletion and page refresh persistence

### V1 Deliverable
✅ Localhost web app where users can add events, watch live countdowns, and receive desktop notifications at the exact scheduled time.

---

## Version 2: Enhancement & Deployment

**Goal:** Improve reliability, add high-value secondary features, address TA feedback, and deploy publicly.

### Enhancements Over V1

| Component | Upgrade | Role |
|-----------|---------|------|
| **Backend** | Add Service Worker support + retry logic + basic rate limiting | Ensures notifications fire even if tab is inactive; handles concurrent users safely |
| **Database** | Migrate to PostgreSQL + add indexes | Production-ready scaling, supports future user accounts & analytics |
| **Client** | Add event sharing links + edit functionality + responsive design | Allows users to share countdowns via URL; improves UX based on TA feedback |

### Implementation Steps

#### 1. Apply TA Feedback from V1 Demo
- [ ] Refactor input validation based on TA suggestions
- [ ] Add loading states for API calls
- [ ] Improve error messages and user feedback
- [ ] Optimize database queries (add indexes on `target_datetime` and `notified`)
- [ ] Fix any bugs or UX issues identified during TA review

#### 2. Event Sharing Feature
- [ ] Generate unique public URLs (`/event/{event_id}`) for each event
- [ ] Create read-only countdown view for shared links
- [ ] Add "Copy Share Link" button to event cards
- [ ] Implement URL-based event retrieval endpoint: `GET /public/event/{event_id}`
- [ ] Test sharing across different browsers and devices

#### 3. Edit Event Functionality
- [ ] Add "Edit" button to event cards
- [ ] Create inline editing or modal form for title and datetime updates
- [ ] Implement `PUT /events/{event_id}` API endpoint
- [ ] Add validation for edit operations
- [ ] Reset `notified` flag when datetime is changed to a future time

#### 4. Notification Reliability Improvements
- [ ] Implement Service Worker for background sync:
  - Register service worker on page load
  - Use `Background Sync API` to trigger notifications when tab is inactive
  - Fallback to periodic polling if background sync unavailable
- [ ] Add retry logic for failed notification attempts
- [ ] Implement basic rate limiting on API endpoints (max 100 requests/minute per IP)
- [ ] Add email notification fallback (optional, using free-tier Mailgun/SendGrid)

#### 5. Database Migration
- [ ] Set up PostgreSQL database (local and production)
- [ ] Write migration script from SQLite to PostgreSQL
- [ ] Update database connection configuration
- [ ] Add database indexes for performance:
  - `idx_events_target_datetime` on `target_datetime`
  - `idx_events_notified` on `notified`
  - `idx_events_session` on `user_session_id`
- [ ] Test with 50+ concurrent countdowns

#### 6. Containerization
- [ ] Write `Dockerfile` for backend:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Create `docker-compose.yml` with services:
  - `backend` (FastAPI app)
  - `db` (PostgreSQL)
  - `nginx` (static files + reverse proxy)
- [ ] Test local deployment with Docker

#### 7. Deployment
- [ ] Choose hosting platform (Render or Railway recommended for free tier)
- [ ] Push code to GitHub repository
- [ ] Connect repository to hosting platform
- [ ] Configure environment variables:
  - `DATABASE_URL` (PostgreSQL connection string)
  - `SECRET_KEY` (for session management)
  - `ALLOWED_HOSTS` (for CORS)
- [ ] Configure HTTPS (required for browser notifications)
- [ ] Set up health check endpoint: `GET /health`
- [ ] Deploy and verify all features work in production

#### 8. Final Testing & Documentation
- [ ] Cross-browser notification test (Chrome, Firefox, Edge, Safari)
- [ ] Timezone validation across different user locations
- [ ] Load test with 50+ concurrent countdowns
- [ ] Test shared links functionality
- [ ] Update `README.md` with:
  - Setup guide
  - Architecture diagram
  - Live demo URL
  - Known limitations and future roadmap

### V2 Deliverable
✅ Publicly accessible, deployed web app with shared links, reliable notifications, and production-grade architecture.

---

## Component Checklist

### Backend (Both Versions)
- [ ] FastAPI application with REST endpoints
- [ ] APScheduler for background tasks
- [ ] Input validation and error handling
- [ ] Time synchronization endpoint
- [ ] Health check endpoint (V2)

### Database (Both Versions)
- [ ] SQLite for V1 local development
- [ ] PostgreSQL for V2 production
- [ ] Proper schema with indexes
- [ ] Migration scripts (V2)

### Client (Both Versions)
- [ ] HTML/CSS/JS web application
- [ ] Real-time countdown rendering
- [ ] Browser Notification API integration
- [ ] Event sharing page (V2)
- [ ] Responsive design

---

## Success Criteria

### Version 1
- ✅ Users can add events with title and datetime
- ✅ Countdowns display and update in real-time
- ✅ Browser notifications fire at scheduled time
- ✅ Events persist across page refreshes
- ✅ TA demo completed and feedback collected

### Version 2
- ✅ TA feedback implemented
- ✅ Events can be edited and shared
- ✅ Notifications work even with inactive tabs
- ✅ App deployed with HTTPS
- ✅ Handles 50+ concurrent users
- ✅ Public URL accessible for live demo
