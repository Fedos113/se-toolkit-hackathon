/**
 * Event Countdown Timer - Frontend Application
 * Handles event CRUD operations and live countdown rendering.
 */

// State
let events = [];
let notificationPermissionGranted = false;

// DOM Elements
let eventForm, eventsContainer, formMessage, titleInput, datetimeInput;

function initDOMElements() {
    eventForm = document.getElementById('event-form');
    eventsContainer = document.getElementById('events-container');
    formMessage = document.getElementById('form-message');
    titleInput = document.getElementById('event-title');
    datetimeInput = document.getElementById('event-datetime');

    if (!eventForm || !eventsContainer || !formMessage || !titleInput || !datetimeInput) {
        console.error('Critical DOM elements not found!');
        return false;
    }
    return true;
}

// API Functions
async function fetchEvents() {
    try {
        const response = await fetch('/events');
        if (!response.ok) throw new Error('Failed to fetch events');
        events = await response.json();
        renderEvents();
    } catch (error) {
        console.error('Error fetching events:', error);
        showMessage('Failed to load events', 'error');
    }
}

async function createEvent(title, targetDatetime) {
    try {
        const response = await fetch('/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                target_datetime: targetDatetime,
                user_session_id: getSessionId()
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create event');
        }

        const event = await response.json();
        events.push(event);
        renderEvents();
        showMessage('Event added successfully!', 'success');
        eventForm.reset();
    } catch (error) {
        console.error('Error creating event:', error);
        showMessage(error.message, 'error');
    }
}

async function deleteEvent(eventId) {
    try {
        const response = await fetch(`/events/${eventId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete event');

        events = events.filter(e => e.id !== eventId);
        renderEvents();
        showMessage('Event deleted', 'success');
    } catch (error) {
        console.error('Error deleting event:', error);
        showMessage('Failed to delete event', 'error');
    }
}

// Notification Functions
function requestNotificationPermission() {
    if (!('Notification' in window)) {
        console.log('This browser does not support desktop notifications');
        return;
    }

    Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
            notificationPermissionGranted = true;
            document.getElementById('notification-btn')?.classList.add('hidden');
            updateNotificationStatus('Notifications enabled!');
        }
    });
}

function showNotification(eventTitle) {
    if (!notificationPermissionGranted) return;

    const notification = new Notification('Event Countdown Timer', {
        body: `${eventTitle} has started!`,
        icon: '⏰',
        tag: eventTitle
    });

    notification.onclick = () => {
        window.focus();
        notification.close();
    };
}

function updateNotificationStatus(text) {
    const statusEl = document.getElementById('notification-status');
    if (statusEl) {
        statusEl.textContent = text;
    }
}

// Session Management
function getSessionId() {
    let sessionId = localStorage.getItem('user_session_id');
    if (!sessionId) {
        sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('user_session_id', sessionId);
    }
    return sessionId;
}

// UI Functions
function showMessage(text, type) {
    formMessage.textContent = text;
    formMessage.className = `message ${type}`;
    
    setTimeout(() => {
        formMessage.classList.add('hidden');
    }, 3000);
}

function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });
}

function getCountdown(targetDatetime) {
    const now = Date.now();
    const target = new Date(targetDatetime).getTime();
    const diff = target - now;

    if (diff <= 0) {
        return { days: 0, hours: 0, minutes: 0, seconds: 0, passed: true };
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    return { days, hours, minutes, seconds, passed: false };
}

function getCountdownState(diff) {
    if (diff <= 0) return 'passed';
    if (diff <= 60000) return 'urgent'; // Less than 1 minute
    if (diff <= 300000) return 'warning'; // Less than 5 minutes
    return '';
}

function renderEvents() {
    if (events.length === 0) {
        eventsContainer.innerHTML = '<p class="empty-state">No events yet. Add your first event above!</p>';
        return;
    }

    eventsContainer.innerHTML = events.map(event => {
        const countdown = getCountdown(event.target_datetime);
        const stateClass = countdown.passed ? 'passed' : '';
        
        return `
            <div class="event-card ${stateClass}" data-id="${event.id}">
                <div class="event-info">
                    <div class="event-title">${escapeHtml(event.title)}</div>
                    <div class="event-datetime">${formatDateTime(event.target_datetime)}</div>
                    <div class="countdown ${stateClass}" id="countdown-${event.id}">
                        ${formatCountdown(countdown)}
                    </div>
                </div>
                <div class="event-actions">
                    <button class="btn-delete" onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </div>
        `;
    }).join('');
}

function formatCountdown({ days, hours, minutes, seconds, passed }) {
    if (passed) {
        return 'Event has passed';
    }
    
    const pad = (n) => String(n).padStart(2, '0');
    return `${pad(days)}d ${pad(hours)}h ${pad(minutes)}m ${pad(seconds)}s`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function updateCountdowns() {
    events.forEach(event => {
        const countdownEl = document.getElementById(`countdown-${event.id}`);
        const cardEl = document.querySelector(`.event-card[data-id="${event.id}"]`);
        
        if (!countdownEl) return;

        const countdown = getCountdown(event.target_datetime);
        const now = Date.now();
        const target = new Date(event.target_datetime).getTime();
        const diff = target - now;
        const stateClass = getCountdownState(diff);

        // Update countdown text
        countdownEl.textContent = formatCountdown(countdown);
        countdownEl.className = `countdown ${stateClass}`;

        // Update card state
        if (cardEl) {
            cardEl.classList.remove('warning', 'urgent', 'passed');
            if (stateClass) {
                cardEl.classList.add(stateClass);
            }
        }

        // Trigger notification if event just passed
        if (countdown.passed && !event.notified && notificationPermissionGranted) {
            showNotification(event.title);
            event.notified = true; // Prevent duplicate notifications
        }
    });
}

// Event Listeners
function handleAddEvent() {
    const title = titleInput.value.trim();
    const targetDatetime = datetimeInput.value;

    if (!title || !targetDatetime) {
        showMessage('Please fill in all fields', 'error');
        return;
    }

    // Validate datetime is in the future
    const targetDate = new Date(targetDatetime);
    const now = new Date();
    if (isNaN(targetDate.getTime())) {
        showMessage('Invalid date format', 'error');
        return;
    }
    if (targetDate <= now) {
        showMessage('Event date must be in the future', 'error');
        return;
    }

    // Convert local datetime to ISO 8601 format with seconds appended
    const isoDatetime = targetDatetime.includes('T') && targetDatetime.split('T')[1].split(':').length === 2
        ? targetDatetime + ':00'
        : targetDatetime;

    createEvent(title, isoDatetime);
}

// Initialize App
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize DOM references
    if (!initDOMElements()) {
        console.error('Failed to initialize DOM elements');
        return;
    }

    // Attach click handler to the Add Event button
    const addBtn = document.getElementById('add-event-btn');
    if (addBtn) {
        addBtn.addEventListener('click', handleAddEvent);
    }

    // Fetch and render events
    await fetchEvents();

    // Update countdowns every second
    setInterval(updateCountdowns, 1000);

    // Check for notification support
    const notifBtn = document.getElementById('notification-btn');
    const notifStatus = document.getElementById('notification-status');
    
    if ('Notification' in window) {
        if (Notification.permission === 'granted') {
            notificationPermissionGranted = true;
            if (notifBtn) notifBtn.style.display = 'none';
            if (notifStatus) notifStatus.textContent = '✅ Notifications enabled!';
            if (notifStatus) notifStatus.style.display = 'block';
        } else if (Notification.permission === 'default') {
            // Show notification permission button
            if (notifBtn) {
                notifBtn.style.display = 'block';
                notifBtn.onclick = requestNotificationPermission;
            }
            if (notifStatus) notifStatus.style.display = 'block';
        } else {
            // Permission denied
            if (notifBtn) notifBtn.style.display = 'none';
            if (notifStatus) {
                notifStatus.textContent = '❌ Notifications blocked by browser. Check browser settings to enable.';
                notifStatus.style.display = 'block';
            }
        }
    } else {
        // Browser doesn't support notifications
        if (notifBtn) notifBtn.style.display = 'none';
        if (notifStatus) {
            notifStatus.textContent = '⚠️ Your browser does not support desktop notifications';
            notifStatus.style.display = 'block';
        }
    }

    // Set minimum datetime to now
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    datetimeInput.min = now.toISOString().slice(0, 16);
});
