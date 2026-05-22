"""
Utility Functions
Rate limiting, analytics tracking, input validation, and other helpers.
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional
import logging
import uuid

from app.config import RATE_LIMIT_CONFIG, UI_CONFIG
from app.api.schemas import HealthStatus, AnalyticsEvent
from app.data.products import get_all_products

logger = logging.getLogger(__name__)


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def init_session_state():
    """Initialize all required session state variables."""
    defaults = {
        "query_input": "",
        "recommendations": None,
        "search_history": [],
        "analytics_events": [],
        "request_times": [],
        "session_id": str(uuid.uuid4()),
        "feedback_given": set(),
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def get_session_id() -> str:
    """Get the current session ID."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id


# ============================================================================
# RATE LIMITING
# ============================================================================

def check_rate_limit() -> tuple[bool, str]:
    """
    Check if the current request is within rate limits.
    
    Returns:
        Tuple of (is_allowed, message)
    """
    now = datetime.now()
    
    if "request_times" not in st.session_state:
        st.session_state.request_times = []
    
    # Clean up old requests outside the window
    cutoff = now - timedelta(minutes=RATE_LIMIT_CONFIG.window_minutes)
    st.session_state.request_times = [
        t for t in st.session_state.request_times if t > cutoff
    ]
    
    # Check if we're at the limit
    current_count = len(st.session_state.request_times)
    if current_count >= RATE_LIMIT_CONFIG.max_requests:
        wait_time = (st.session_state.request_times[0] + timedelta(minutes=RATE_LIMIT_CONFIG.window_minutes) - now).seconds
        return False, f"Rate limit reached. Please wait {wait_time} seconds."
    
    # Record this request
    st.session_state.request_times.append(now)
    
    remaining = RATE_LIMIT_CONFIG.max_requests - current_count - 1
    return True, f"{remaining} requests remaining"


def get_rate_limit_status() -> dict:
    """Get current rate limit status."""
    now = datetime.now()
    cutoff = now - timedelta(minutes=RATE_LIMIT_CONFIG.window_minutes)
    
    if "request_times" not in st.session_state:
        st.session_state.request_times = []
    
    recent_requests = [t for t in st.session_state.request_times if t > cutoff]
    
    return {
        "requests_used": len(recent_requests),
        "requests_limit": RATE_LIMIT_CONFIG.max_requests,
        "requests_remaining": max(0, RATE_LIMIT_CONFIG.max_requests - len(recent_requests)),
        "window_minutes": RATE_LIMIT_CONFIG.window_minutes,
    }


# ============================================================================
# SEARCH HISTORY
# ============================================================================

def add_to_search_history(query: str, source: str, results_count: int):
    """Add a search to the history."""
    if "search_history" not in st.session_state:
        st.session_state.search_history = []
    
    entry = {
        "query": query,
        "source": source,
        "results_count": results_count,
        "timestamp": datetime.now().isoformat(),
    }
    
    # Add to front, limit to 10 entries
    st.session_state.search_history.insert(0, entry)
    st.session_state.search_history = st.session_state.search_history[:10]


def get_search_history() -> list[dict]:
    """Get the search history."""
    return st.session_state.get("search_history", [])


def clear_search_history():
    """Clear the search history."""
    st.session_state.search_history = []


# ============================================================================
# ANALYTICS
# ============================================================================

def track_event(event_name: str, properties: Optional[dict] = None):
    """
    Track an analytics event.
    Events are stored in session state for this demo.
    In production, send to analytics service.
    """
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    event = AnalyticsEvent(
        event_name=event_name,
        properties=properties or {},
        timestamp=datetime.now().isoformat(),
        session_id=get_session_id(),
    )
    
    st.session_state.analytics_events.append(event.model_dump())
    logger.debug(f"Tracked event: {event_name}")


def get_analytics_summary() -> dict:
    """Get a summary of tracked events."""
    events = st.session_state.get("analytics_events", [])
    
    event_counts = {}
    for event in events:
        name = event["event_name"]
        event_counts[name] = event_counts.get(name, 0) + 1
    
    return {
        "total_events": len(events),
        "event_counts": event_counts,
        "session_id": get_session_id(),
    }


# ============================================================================
# FEEDBACK
# ============================================================================

def record_feedback(recommendation_id: str, feedback_type: str):
    """
    Record user feedback on a recommendation.
    
    Args:
        recommendation_id: The product ID that was recommended
        feedback_type: "positive" or "negative"
    """
    if "feedback_given" not in st.session_state:
        st.session_state.feedback_given = set()
    
    # Prevent duplicate feedback
    if recommendation_id in st.session_state.feedback_given:
        return False
    
    st.session_state.feedback_given.add(recommendation_id)
    
    track_event("recommendation_feedback", {
        "product_id": recommendation_id,
        "feedback_type": feedback_type,
    })
    
    logger.info(f"Feedback recorded: {recommendation_id} = {feedback_type}")
    return True


def has_given_feedback(recommendation_id: str) -> bool:
    """Check if feedback was already given for a recommendation."""
    return recommendation_id in st.session_state.get("feedback_given", set())


# ============================================================================
# HEALTH CHECK
# ============================================================================

def get_health_status() -> HealthStatus:
    """Get the system health status."""
    from app.config import is_api_configured
    
    products = get_all_products()
    
    return HealthStatus(
        status="healthy",
        api_configured=is_api_configured(),
        products_count=len(products),
        cache_enabled=True,
        timestamp=datetime.now().isoformat(),
    )


# ============================================================================
# INPUT VALIDATION
# ============================================================================

def validate_query(query: str) -> tuple[bool, str]:
    """
    Validate user query input.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not query:
        return False, "Please enter your preferences"
    
    query = query.strip()
    
    if len(query) < 3:
        return False, "Query too short. Please be more specific."
    
    if len(query) > UI_CONFIG.max_query_length:
        return False, f"Query too long. Maximum {UI_CONFIG.max_query_length} characters."
    
    # Check for suspicious patterns (basic XSS prevention)
    suspicious_patterns = ["<script", "javascript:", "onclick", "onerror"]
    query_lower = query.lower()
    for pattern in suspicious_patterns:
        if pattern in query_lower:
            return False, "Invalid characters in query"
    
    return True, ""


def sanitize_query(query: str) -> str:
    """
    Sanitize user query input.
    Removes potentially dangerous characters.
    """
    import html
    import re
    
    # Strip and escape HTML
    query = html.escape(query.strip())
    
    # Remove control characters and unusual whitespace
    query = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
    
    # Remove potentially dangerous characters
    query = re.sub(r'[<>{}\\`]', '', query)
    
    # Normalize whitespace
    query = ' '.join(query.split())
    
    return query[:UI_CONFIG.max_query_length]
