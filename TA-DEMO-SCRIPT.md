# TA Demo Script — Event Countdown Timer

## Quick Pitch (30 seconds)

> "Event Countdown Timer is a simple web app where you add events with a target date and time, watch live countdowns ticking down to the second, and get a desktop notification the moment each event starts. It solves the problem of missing deadlines because you forget to check your calendar."

**End-user:** Students, professionals, anyone who tracks deadlines.
**One sentence:** "A web page where you add events, watch live countdowns, and get notified when they arrive."
**Core feature:** Real-time live countdown display with automatic desktop notifications.

---

## 3-Minute Live Demo

### Step 1: Show the app (30 sec)
1. Open browser to `http://localhost:8000`
2. Point out the clean UI: form at top, events list below
3. Mention: "No login, no signup — just open and use"

### Step 2: Add an event (30 sec)
1. Type title: `"TA Demo Event"`
2. Pick a date **2-3 minutes in the future**
3. Click **"Add Event"**
4. Point out: success message, event appears in list, countdown starts immediately

### Step 3: Show the countdown live (30 sec)
1. Watch the seconds ticking down
2. Show that the event card is blue (normal state)
3. Mention: "All data is stored in SQLite — survives page refresh"
4. **Refresh the page** to prove persistence

### Step 4: Show visual state changes (30 sec)
1. When countdown drops below 5 minutes → card border turns **yellow** (warning)
2. When countdown drops below 1 minute → card border turns **red** + **pulse animation** (urgent)
3. Say: "Visual feedback so you can see at a glance how close an event is"

### Step 5: Fire the notification (30 sec)
1. When countdown hits `00:00:00` → desktop notification pops up
2. Notification says: **"TA Demo Event has started!"**
3. Mention: "Background scheduler also checks every 30 seconds server-side, so notifications fire even if the browser tab is closed"

### Step 6: Delete and API (30 sec)
1. Click **Delete** on the event
2. Event disappears, success message shown
3. Open `http://localhost:8000/docs` (Swagger UI)
4. Show the API endpoints: `GET /events`, `POST /events`, `DELETE /events/{id}`, `GET /server-time`
5. Say: "Full REST API — can be integrated with any frontend"

---

## Architecture Overview (for TA questions)

| Layer | Technology | File |
|-------|-----------|------|
| **Backend** | Python + FastAPI | `main.py` — 6 endpoints, CORS, startup hooks |
| **Database** | SQLite | `database.py` — 8 functions, auto-init on import |
| **Scheduler** | APScheduler | `scheduler.py` — scans DB every 30s for past events |
| **Frontend** | Vanilla HTML/CSS/JS | `static/` — SPA with fetch API, setInterval, Notification API |

**Database schema:**
```sql
events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    target_datetime TEXT NOT NULL,    -- ISO 8601
    created_at TEXT NOT NULL,          -- ISO 8601
    user_session_id TEXT,              -- nullable
    notified BOOLEAN DEFAULT 0
)
```

---

## V1 vs V2 Comparison

| Feature | V1 (MVP) | V2 (Polish) |
|---------|----------|-------------|
| Add/Delete events | ✅ | ✅ |
| Live countdown | ✅ | ✅ |
| SQLite persistence | ✅ | ✅ |
| Desktop notifications | ❌ | ✅ Browser Notification API |
| Background scheduler | ❌ | ✅ APScheduler every 30s |
| Visual urgency states | ❌ | ✅ Blue → Yellow → Red |
| Server-client time sync | ❌ | ✅ `/server-time` endpoint |
| Responsive mobile CSS | ❌ | ✅ Media queries |
| Notification tracking | ❌ | ✅ `notified` flag in DB |

---

## Common TA Questions & Answers

**Q: Why this project?**
A: It's simple to explain but demonstrates all required layers (backend, DB, client). Everyone understands countdowns.

**Q: What happens if the server restarts?**
A: The scheduler restarts with the server. Events that passed while the server was down get notified immediately on startup.

**Q: How do notifications work if the tab is closed?**
A: The APScheduler runs server-side every 30 seconds. It marks events as `notified = true` in the database. When the user reopens the app, the frontend sees `notified: true` and won't double-fire.

**Q: Can multiple users share this?**
A: Currently it's localhost single-user. The `user_session_id` field is already in the database for future multi-user support.

**Q: What would you add next?**
A: User accounts, recurring events, timezone selector, event sharing via URL, email/SMS notifications.

---

## Checklist Before Demo

- [ ] Server running: `python -m uvicorn main:app --host 127.0.0.1 --port 8000`
- [ ] Browser open at `http://localhost:8000`
- [ ] Swagger UI ready at `http://localhost:8000/docs`
- [ ] Notification permission granted in browser
- [ ] Practice adding an event 2-3 minutes in the future
- [ ] AUDIT.md and IMPLEMENTATION-PLAN.md updated (done ✅)
- [ ] This script printed or on second screen
