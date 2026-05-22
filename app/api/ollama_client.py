"""
Ollama API Client
Production-ready API client with retry logic, timeout handling, and structured responses.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
import logging

from app.config import API_CONFIG, get_api_key
from app.api.schemas import RecommendationResponse, RecommendationItem

logger = logging.getLogger(__name__)


class OllamaAPIError(Exception):
    """Custom exception for Ollama API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def create_session() -> requests.Session:
    """
    Create a requests session with retry logic.
    Implements exponential backoff for transient failures.
    """
    session = requests.Session()
    
    retry_strategy = Retry(
        total=API_CONFIG.max_retries,
        backoff_factor=API_CONFIG.retry_backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=False
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session


def build_system_prompt() -> str:
    """Build the system prompt for the AI model."""
    return """You are an expert product recommendation assistant. Your task is to recommend products ONLY from the provided catalog based on user preferences.

STRICT RULES:
1. ONLY recommend products that exist in the provided catalog
2. NEVER invent or suggest products outside the catalog
3. Return ONLY valid JSON matching the exact schema below
4. Provide 1-3 recommendations based on relevance
5. Match scores should be 0-100 based on how well the product fits the user's needs
6. Be concise but informative in your reasons

OUTPUT SCHEMA (return ONLY this JSON, no other text):
{
  "recommendations": [
    {
      "product_id": "exact-id-from-catalog",
      "match_score": 85,
      "reason": "Brief explanation of why this product matches the user's needs"
    }
  ],
  "summary": "Brief overall summary of recommendations"
}"""


def build_catalog_prompt(products: list[dict]) -> str:
    """Build the product catalog text for the prompt."""
    catalog_lines = []
    for p in products:
        specs_str = ", ".join(f"{k}: {v}" for k, v in p.get("specs", {}).items())
        tags_str = ", ".join(p.get("tags", []))
        catalog_lines.append(
            f"ID: {p['id']} | {p['name']} | {p['category']} | ${p['price']} | "
            f"Rating: {p['rating']}★ | {p['description']} | Specs: {specs_str} | "
            f"Best for: {p.get('best_for', '')} | Tags: {tags_str}"
        )
    return "\n".join(catalog_lines)


def call_ollama_api(user_query: str, products: list[dict]) -> RecommendationResponse:
    """
    Call the Ollama API to get AI-powered recommendations.
    
    Args:
        user_query: The user's natural language query
        products: List of product dictionaries
        
    Returns:
        RecommendationResponse with AI recommendations
        
    Raises:
        OllamaAPIError: If API call fails
    """
    api_key = get_api_key()
    if not api_key:
        raise OllamaAPIError("API key not configured")
    
    catalog_text = build_catalog_prompt(products)
    system_prompt = build_system_prompt()
    
    user_prompt = f"""PRODUCT CATALOG:
{catalog_text}

USER REQUEST: {user_query}

Analyze the user's request and recommend the best matching products from the catalog above. Return ONLY valid JSON."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": API_CONFIG.model,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    session = create_session()
    
    try:
        logger.info(f"Calling Ollama API with query: {user_query[:50]}...")
        
        response = session.post(
            API_CONFIG.base_url,
            headers=headers,
            json=payload,
            timeout=API_CONFIG.timeout
        )
        
        if response.status_code != 200:
            logger.error(f"API returned status {response.status_code}: {response.text[:200]}")
            raise OllamaAPIError(
                f"API request failed with status {response.status_code}",
                status_code=response.status_code
            )
        
        result = response.json()
        
        # Extract content from response
        if "message" in result and "content" in result["message"]:
            content = result["message"]["content"]
        elif "response" in result:
            content = result["response"]
        else:
            raise OllamaAPIError("Unexpected API response structure")
        
        # Parse JSON content
        parsed = json.loads(content)
        
        # Validate and build response
        recommendations = []
        for rec in parsed.get("recommendations", []):
            try:
                item = RecommendationItem(
                    product_id=rec["product_id"],
                    match_score=rec.get("match_score", 50),
                    reason=rec.get("reason", "Recommended based on your preferences")
                )
                recommendations.append(item)
            except Exception as e:
                logger.warning(f"Skipping invalid recommendation: {e}")
                continue
        
        logger.info(f"API returned {len(recommendations)} recommendations")
        
        return RecommendationResponse(
            recommendations=recommendations,
            summary=parsed.get("summary", ""),
            source="ai"
        )
        
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        raise OllamaAPIError("Request timed out")
    except requests.exceptions.ConnectionError:
        logger.error("API connection error")
        raise OllamaAPIError("Connection error")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        raise OllamaAPIError("Invalid JSON response from API")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise OllamaAPIError(str(e))
