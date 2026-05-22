"""
Ollama API Client
Production-ready API client for Ollama with Gemma model.
"""

import json
import logging
import requests
from typing import Optional

from app.config import API_CONFIG, get_api_key
from app.api.schemas import RecommendationResponse, RecommendationItem

logger = logging.getLogger(__name__)


class OllamaAPIError(Exception):
    """Custom exception for Ollama API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def build_prompt(user_query: str, products: list[dict]) -> str:
    """Build the complete prompt for Ollama."""
    
    # Build product catalog
    catalog_lines = []
    for p in products:
        specs_str = ", ".join(f"{k}: {v}" for k, v in p.get("specs", {}).items())
        tags_str = ", ".join(p.get("tags", []))
        catalog_lines.append(
            f"ID: {p['id']} | {p['name']} | {p['category']} | ${p['price']} | "
            f"Rating: {p['rating']}★ | {p['description']} | Specs: {specs_str} | "
            f"Best for: {p.get('best_for', '')} | Tags: {tags_str}"
        )
    catalog_text = "\n".join(catalog_lines)
    
    prompt = f"""You are an expert product recommendation assistant. Your task is to recommend products ONLY from the provided catalog based on user preferences.

STRICT RULES:
1. ONLY recommend products that exist in the provided catalog
2. NEVER invent or suggest products outside the catalog
3. Return ONLY valid JSON matching the exact schema below
4. Provide 1-3 recommendations based on relevance
5. Match scores should be 0-100 based on how well the product fits the user's needs
6. Be concise but informative in your reasons

PRODUCT CATALOG:
{catalog_text}

USER REQUEST: {user_query}

OUTPUT FORMAT (return ONLY this JSON, no other text, no markdown code blocks):
{{"recommendations": [{{"product_id": "exact-id-from-catalog", "match_score": 85, "reason": "Brief explanation"}}], "summary": "Brief overall summary"}}

Analyze the user's request and recommend the best matching products. Return ONLY the JSON object."""

    return prompt


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
    
    try:
        # Build prompt
        prompt = build_prompt(user_query, products)
        
        logger.info(f"Calling Ollama API with query: {user_query[:50]}...")
        
        # Prepare request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": API_CONFIG.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        # Make request
        response = requests.post(
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
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
        elif "message" in result and "content" in result["message"]:
            content = result["message"]["content"]
        else:
            raise OllamaAPIError("Unexpected API response structure")
        
        content = content.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        # Parse JSON
        parsed = json.loads(content)
        
        # Build response
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
        
        logger.info(f"Ollama returned {len(recommendations)} recommendations")
        
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
        logger.error(f"Ollama API error: {e}")
        raise OllamaAPIError(str(e))


# Alias for compatibility
GeminiAPIError = OllamaAPIError
call_gemini_api = call_ollama_api
