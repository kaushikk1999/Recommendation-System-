"""
Gemini API Client
Production-ready API client for Google's Gemini AI.
"""

import json
import logging
from typing import Optional

import google.generativeai as genai

from app.config import API_CONFIG, get_api_key
from app.api.schemas import RecommendationResponse, RecommendationItem

logger = logging.getLogger(__name__)


class GeminiAPIError(Exception):
    """Custom exception for Gemini API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def build_prompt(user_query: str, products: list[dict]) -> str:
    """Build the complete prompt for Gemini."""
    
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


def call_gemini_api(user_query: str, products: list[dict]) -> RecommendationResponse:
    """
    Call the Gemini API to get AI-powered recommendations.
    
    Args:
        user_query: The user's natural language query
        products: List of product dictionaries
        
    Returns:
        RecommendationResponse with AI recommendations
        
    Raises:
        GeminiAPIError: If API call fails
    """
    api_key = get_api_key()
    if not api_key:
        raise GeminiAPIError("API key not configured")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel(API_CONFIG.model)
        
        # Build prompt
        prompt = build_prompt(user_query, products)
        
        logger.info(f"Calling Gemini API with query: {user_query[:50]}...")
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=1024,
            )
        )
        
        # Extract text
        content = response.text.strip()
        
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
        
        logger.info(f"Gemini returned {len(recommendations)} recommendations")
        
        return RecommendationResponse(
            recommendations=recommendations,
            summary=parsed.get("summary", ""),
            source="ai"
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        raise GeminiAPIError("Invalid JSON response from API")
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise GeminiAPIError(str(e))


# Alias for backward compatibility
OllamaAPIError = GeminiAPIError
call_ollama_api = call_gemini_api
