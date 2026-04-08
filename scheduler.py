"""
Event Countdown Timer - Notification Scheduler
Background task scheduler for monitoring event notifications.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import database

scheduler = BackgroundScheduler()


def check_past_events():
    """Scan for events that have passed but haven't been notified yet."""
    try:
        past_events = database.get_unnotified_past_events()
        
        for event in past_events:
            # Mark as notified in database
            database.update_event_notified(event['id'])
            print(f"[{datetime.utcnow().isoformat()}] Event notified: {event['title']} (ID: {event['id']})")
            
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
