# Event Countdown Timer - Deployment Verification

## Prerequisites Checklist

### Required Software
- [ ] **Python 3.8+** installed
  - Download from: https://www.python.org/downloads/
  - During installation, check **"Add Python to PATH"**
  - Verify: Run `python --version` in terminal

## Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   - [ ] fastapi installed
   - [ ] uvicorn installed
   - [ ] APScheduler installed

3. **Start the Server**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```
   
   **OR** (Windows users):
   ```bash
   start.bat
   ```

## Verification Tests

### Test 1: Server Startup
- [ ] Server starts without errors
- [ ] Console shows: "Scheduler started - scanning every 30 seconds"
- [ ] Access http://localhost:8000 in browser
- [ ] Main page loads with the Event Countdown Timer UI

### Test 2: API Endpoints
Open browser to http://localhost:8000/docs to see Swagger UI

**Test GET /server-time:**
```bash
curl http://localhost:8000/server-time
```
Expected: `{"server_time": "2026-04-08T..."}`

**Test POST /events:**
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Event", "target_datetime": "2026-04-08T20:00:00"}'
```
Expected: Event object with id, title, target_datetime, etc.

**Test GET /events:**
```bash
curl http://localhost:8000/events
```
Expected: Array of events including the one just created

**Test DELETE /events/1:**
```bash
curl -X DELETE http://localhost:8000/events/1
```
Expected: `{"message": "Event deleted successfully"}`

### Test 3: Frontend Functionality (V1)
- [ ] Page displays form to add events
- [ ] Can enter event title
- [ ] Can select date/time picker
- [ ] "Add Event" button creates event
- [ ] Event appears in list below
- [ ] Live countdown updates every second
- [ ] Countdown shows days, hours, minutes, seconds
- [ ] Delete button removes event from list and database
- [ ] Events persist after page refresh

### Test 4: Notifications (V2)
- [ ] "Enable Desktop Notifications" button appears
- [ ] Clicking button triggers browser permission request
- [ ] After granting permission, button disappears
- [ ] Create an event 1-2 minutes in the future
- [ ] Countdown updates with visual state changes:
  - Blue: Normal (>5 minutes)
  - Yellow/Orange: Warning (1-5 minutes)
  - Red + Pulse: Urgent (<1 minute)
- [ ] Desktop notification fires at exactly 00:00:00
- [ ] Notification shows event title + "has started!"
- [ ] Event marked as notified (no duplicate notifications)

### Test 5: Background Scheduler (V2)
- [ ] Server console shows scheduler started message
- [ ] Events that passed while server was running get notified
- [ ] Scheduler continues running in background
- [ ] Server restart doesn't cause duplicate notifications

### Test 6: Responsive Design (V2)
- [ ] Page looks good on desktop browser
- [ ] Resize browser window to mobile size (or use DevTools)
- [ ] Layout adapts for mobile
- [ ] Form inputs are usable on small screens
- [ ] Event cards stack vertically on mobile

## Environment Variables (Optional)

The application works out of the box with defaults. To customize:

1. Copy `.env.example` to `.env`
2. Edit values as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `8000` | Server port |
| `DATABASE_PATH` | `./events.db` | SQLite database file location |
| `NOTIFICATION_CHECK_INTERVAL` | `30` | Seconds between scheduler checks |

**Note:** The current implementation doesn't load `.env` files automatically. If you need environment variable support, install `python-dotenv`:

```bash
pip install python-dotenv
```

And add to `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Common Issues & Solutions

### Python not found
- Install Python from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Restart terminal after installation

### Port 8000 already in use
- Change port: `uvicorn main:app --reload --port 8001`
- Or kill process using port 8000

### Notifications not working
- Check browser permissions
- HTTPS required for some browsers (localhost works)
- Test in Chrome/Edge/Firefox (Safari has limited support)

### Database errors
- Delete `events.db` to reset
- Database auto-creates on first run

## Demo Checklist (for TA Presentation)

- [ ] Application starts successfully
- [ ] Can add events with future dates
- [ ] Countdown displays and updates live
- [ ] Visual color changes as event approaches
- [ ] Desktop notification fires at exact time
- [ ] Events persist across page refreshes
- [ ] Can delete events
- [ ] UI is responsive on different screen sizes
- [ ] 3-minute demo: Add event 3 min away → wait → notification fires

## Success Criteria

✅ **V1 Complete When:**
- Events can be added and deleted
- Live countdown updates every second
- Data persists in SQLite database
- Basic UI is functional

✅ **V2 Complete When:**
- All V1 features working
- Desktop notifications fire on time
- Background scheduler running
- Visual state changes (colors)
- Server-client time sync working
- Responsive design functional
- Ready for TA demo
