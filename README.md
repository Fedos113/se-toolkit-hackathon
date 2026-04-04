# Event Countdown Timer

A lightweight web app that turns important dates into live visual countdowns and triggers browser notifications so you never miss a deadline.

## Product Context

### End Users
- **Students** tracking exam dates, assignment deadlines, and project milestones
- **Remote workers** managing deliverables and meeting schedules
- **Event coordinators** monitoring event start times and preparation deadlines

### Problem
Important dates get buried in calendars or notes, causing last-minute panic or missed deadlines due to lack of visual urgency and timely alerts.

### Solution
A lightweight web app that turns important dates into live visual countdowns and triggers browser notifications so you never miss a deadline.

## Features

### Implemented
- ✅ Create, view, and delete events with target dates
- ✅ Real-time countdown display synced to server time
- ✅ Browser push notifications when countdown reaches zero
- ✅ Persistent event storage using SQLite
- ✅ Clean, responsive dashboard UI
- ✅ Background scheduler to prevent duplicate notifications

### Not Yet Implemented
- 🔲 Event sharing via unique public URLs
- 🔲 Edit existing events
- 🔲 Service Worker support for background notifications
- 🔲 Email notification fallback
- 🔲 PostgreSQL migration
- 🔲 User authentication and multi-user support
- 🔲 Rate limiting and retry logic

## Usage

1. **Start the application** (see Deployment section below)
2. **Open your browser** and navigate to `http://localhost:8000`
3. **Add a new event** by entering a title and selecting the target date/time
4. **Watch the countdown** update in real-time on your dashboard
5. **Allow browser notifications** when prompted to receive alerts when events start
6. **Delete events** you no longer need to track

## Deployment

### Operating System
- **Ubuntu 24.04 LTS** (recommended, matching university VMs)
- Also compatible with Windows and macOS

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, or Edge recommended for notifications)

### Step-by-Step Deployment Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd se-toolkit-hackathon
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   - The app uses SQLite by default (no additional configuration needed)
   - Database file will be created automatically on first run

4. **Start the backend server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - On first visit, you'll be prompted to allow browser notifications - click "Allow"

6. **(Optional) Run in production mode**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Production Deployment (Render/Railway)
1. Push your code to a GitHub repository
2. Connect to Render or Railway
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy and access via the provided HTTPS URL

> **Note:** HTTPS is required for browser notifications to work in production.
