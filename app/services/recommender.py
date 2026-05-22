"""
Recommendation Service
Combines AI-powered and fallback recommendation engines.
Handles caching, error recovery, and source selection.
"""

import logging
import time
import streamlit as st
from typing import Optional

from app.config import get_api_key, CACHE_CONFIG
from app.api.schemas import RecommendationResponse, UserQuery
from app.api.ollama_client import call_ollama_api, OllamaAPIError
from app.services.fallback import fallback_recommend
from app.data.products import get_all_products

logger = logging.getLogger(__name__)


def _get_cache_key(query: str, category: Optional[str], budget: Optional[int]) -> str:
    """Generate a cache key for the recommendation request."""
    return f"{query}|{category or 'all'}|{budget or 'none'}"


@st.cache_data(ttl=CACHE_CONFIG.recommendations_ttl, show_spinner=False)
def _cached_recommendation(cache_key: str, query: str, use_ai: bool) -> dict:
    """
    Internal cached recommendation function.
    Returns dict that can be serialized by Streamlit cache.
    """
    products = get_all_products()
    
    if use_ai:
        try:
            start_time = time.time()
            result = call_ollama_api(query, products)
            latency_ms = (time.time() - start_time) * 1000
            logger.info(f"AI recommendation completed in {latency_ms:.2f}ms")
            return result.model_dump()
        except OllamaAPIError as e:
            logger.warning(f"AI API failed, falling back: {e.message}")
            result = fallback_recommend(query, products)
            result.warning = f"AI unavailable: {e.message}. Using smart fallback."
            return result.model_dump()
    else:
        result = fallback_recommend(query, products)
        result.warning = "API key not configured. Using smart fallback engine."
        return result.model_dump()


def get_recommendations(
    user_query: UserQuery,
    force_fallback: bool = False
) -> RecommendationResponse:
    """
    Get product recommendations based on user query.
    
    Args:
        user_query: Validated user query object
        force_fallback: If True, skip AI and use fallback only
        
    Returns:
        RecommendationResponse with recommendations and metadata
    """
    # Build the enhanced query with filters
    enhanced_query = user_query.text
    if user_query.category_filter and user_query.category_filter != "All Categories":
        enhanced_query += f" in {user_query.category_filter} category"
    if user_query.max_budget and user_query.max_budget < 10000:
        enhanced_query += f" under ${user_query.max_budget}"
    
    # Determine if we should try AI
    use_ai = not force_fallback and bool(get_api_key())
    
    # Generate cache key
    cache_key = _get_cache_key(
        enhanced_query,
        user_query.category_filter,
        user_query.max_budget
    )
    
    # Get cached or fresh recommendations
    result_dict = _cached_recommendation(cache_key, enhanced_query, use_ai)
    
    # Convert back to Pydantic model
    return RecommendationResponse(**result_dict)


def clear_recommendation_cache():
    """Clear the recommendation cache."""
    _cached_recommendation.clear()
    logger.info("Recommendation cache cleared")


def get_recommendation_stats() -> dict:
    """Get statistics about the recommendation system."""
    products = get_all_products()
    categories = list(set(p["category"] for p in products))
    
    return {
        "total_products": len(products),
        "categories": len(categories),
        "category_list": categories,
        "ai_available": bool(get_api_key()),
        "cache_ttl_seconds": CACHE_CONFIG.recommendations_ttl,
    }
