"""
Application Configuration
Centralized configuration management with environment variable support.
"""

import os
import streamlit as st
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class APIConfig:
    """Gemini API configuration."""
    model: str = "gemini-1.5-flash"
    timeout: int = 30
    max_retries: int = 3
    retry_backoff: float = 0.5


@dataclass(frozen=True)
class RateLimitConfig:
    """Rate limiting configuration."""
    max_requests: int = 10
    window_minutes: int = 1


@dataclass(frozen=True)
class CacheConfig:
    """Caching configuration."""
    recommendations_ttl: int = 300  # 5 minutes
    products_ttl: int = 3600  # 1 hour


@dataclass(frozen=True)
class UIConfig:
    """UI configuration."""
    max_query_length: int = 500
    max_recommendations: int = 5
    default_recommendations: int = 3


# Global configuration instances
API_CONFIG = APIConfig()
RATE_LIMIT_CONFIG = RateLimitConfig()
CACHE_CONFIG = CacheConfig()
UI_CONFIG = UIConfig()


def get_api_key() -> Optional[str]:
    """
    Securely retrieve API key from Streamlit secrets or environment.
    Priority: st.secrets > environment variable
    """
    # Try Streamlit secrets first
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass
    
    # Fallback to environment variable
    return os.getenv("GEMINI_API_KEY")


def is_api_configured() -> bool:
    """Check if API key is configured."""
    return bool(get_api_key())
