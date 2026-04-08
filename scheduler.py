"""
Event Countdown Timer - Notification Scheduler
Background task scheduler for monitoring event notifications.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import database

scheduler = BackgroundScheduler()


def check_past_events():
    """Scan for events that have passed but haven't been notified yet, grouped by user session."""
    try:
        # Get all unique session IDs that have unnotified past events
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        now = datetime.utcnow().isoformat()
        cursor.execute(
            "SELECT DISTINCT user_session_id FROM events WHERE target_datetime <= ? AND notified = 0 AND user_session_id IS NOT NULL",
            (now,)
        )
        session_ids = [row['user_session_id'] for row in cursor.fetchall()]
        conn.close()
        
        # For each session, get and notify their past events
        for session_id in session_ids:
            past_events = database.get_unnotified_past_events_by_session_id(session_id)
            
            for event in past_events:
                # Mark as notified in database
                database.update_event_notified(event['id'])
                print(f"[{datetime.utcnow().isoformat()}] Event notified: {event['title']} (ID: {event['id']}, Session: {session_id})")

    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Error checking events: {e}")


def start_scheduler():
    """Start the background scheduler to scan for events every 30 seconds."""
    scheduler.add_job(
        check_past_events,
        'interval',
        seconds=30,
        id='check_past_events',
        replace_existing=True,
        max_instances=1
    )
    scheduler.start()
    print(f"[{datetime.utcnow().isoformat()}] Scheduler started - scanning every 30 seconds")


def stop_scheduler():
    """Stop the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        print(f"[{datetime.utcnow().isoformat()}] Scheduler stopped")
