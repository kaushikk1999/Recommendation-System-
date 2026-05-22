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
    """Ollama API configuration (local)."""
    base_url: str = "http://localhost:11434/api/chat"
    model: str = "gemma2"
    timeout: int = 120
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
        key = st.secrets.get("OLLAMA_API_KEY")
        if key:
            return key
    except Exception:
        pass
    
    # Fallback to environment variable
    return os.getenv("OLLAMA_API_KEY")


def is_api_configured() -> bool:
    """Check if Ollama is available (local doesn't need API key)."""
    # Local Ollama doesn't require API key
    return True
