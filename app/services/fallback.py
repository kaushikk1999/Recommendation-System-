"""
Fallback Recommendation Engine
Deterministic recommendation system that works without AI API.
Uses keyword matching, budget analysis, and rating-based ranking.
"""

import re
from typing import Optional
import logging

from app.api.schemas import RecommendationResponse, RecommendationItem

logger = logging.getLogger(__name__)


# Category keyword mappings for natural language understanding
CATEGORY_KEYWORDS = {
    "phone": ["phone", "smartphone", "mobile", "iphone", "android", "pixel", "galaxy", "cellular"],
    "laptop": ["laptop", "notebook", "computer", "macbook", "chromebook", "ultrabook"],
    "headphones": ["headphones", "earbuds", "earphones", "headset", "audio", "music", "listening"],
    "smartwatch": ["smartwatch", "watch", "fitness tracker", "wearable", "fitbit", "fitness band"],
    "tablet": ["tablet", "ipad", "tab", "slate"],
    "accessories": ["accessory", "charger", "stand", "powerbank", "cable", "dock", "hub"],
}


def parse_budget_from_query(query: str) -> Optional[int]:
    """
    Extract budget amount from natural language query.
    
    Examples:
        "phone under $500" -> 500
        "laptop below 1000" -> 1000
        "headphones max $200" -> 200
    """
    patterns = [
        r'under\s*\$?(\d+)',
        r'below\s*\$?(\d+)',
        r'less\s+than\s*\$?(\d+)',
        r'max(?:imum)?\s*\$?(\d+)',
        r'budget\s*(?:of|is|:)?\s*\$?(\d+)',
        r'\$(\d+)\s*(?:or\s+less|max|budget)',
        r'up\s+to\s*\$?(\d+)',
        r'within\s*\$?(\d+)',
        r'around\s*\$?(\d+)',
        r'about\s*\$?(\d+)',
    ]
    
    query_lower = query.lower()
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            return int(match.group(1))
    return None


def extract_category_hints(query: str) -> list[str]:
    """
    Extract category hints from the query using keyword matching.
    
    Returns list of matching category keys (not display names).
    """
    query_lower = query.lower()
    found = []
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            found.append(category)
    
    return found


def calculate_text_match_score(product: dict, query: str) -> float:
    """
    Calculate how well a product matches the query text.
    Uses multiple signals for robust matching.
    """
    score = 0.0
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]
    
    # Name matching (high weight)
    name_lower = product["name"].lower()
    for word in query_words:
        if word in name_lower:
            score += 25
    
    # Description matching (medium weight)
    desc_lower = product["description"].lower()
    for word in query_words:
        if word in desc_lower:
            score += 8
    
    # Tag matching (high weight - most specific)
    for tag in product.get("tags", []):
        tag_lower = tag.lower()
        if tag_lower in query_lower:
            score += 20
        # Partial tag match
        for word in query_words:
            if word in tag_lower or tag_lower in word:
                score += 10
    
    # Best-for matching (high weight)
    best_for_lower = product.get("best_for", "").lower()
    for word in query_words:
        if word in best_for_lower:
            score += 15
    
    # Specs matching (medium weight)
    specs_text = " ".join(str(v).lower() for v in product.get("specs", {}).values())
    for word in query_words:
        if word in specs_text:
            score += 5
    
    return score


def calculate_budget_score(product: dict, budget: Optional[int]) -> float:
    """
    Calculate budget fit score.
    Rewards products that are under budget but close to it (better value).
    """
    if budget is None:
        return 0.0
    
    price = product["price"]
    
    if price <= budget:
        # Under budget - reward higher utilization (better value)
        utilization = price / budget
        return 20 * utilization
    else:
        # Over budget - penalty proportional to how much over
        overage = (price - budget) / budget
        return -30 * min(overage, 1.0)


def calculate_quality_score(product: dict) -> float:
    """
    Calculate quality score based on rating.
    """
    rating = product.get("rating", 3.0)
    # Scale from 0-5 rating to bonus points
    return (rating - 3.0) * 10  # Range: -20 to +20


def fallback_recommend(
    query: str,
    products: list[dict],
    max_results: int = 3
) -> RecommendationResponse:
    """
    Generate recommendations using the fallback engine.
    
    Algorithm:
    1. Parse budget from query
    2. Extract category hints
    3. Filter by category if detected
    4. Filter by budget if specified
    5. Score remaining products
    6. Return top N with generated reasons
    """
    logger.info(f"Fallback engine processing: {query[:50]}...")
    
    budget = parse_budget_from_query(query)
    category_hints = extract_category_hints(query)
    
    # Start with all products
    candidates = products.copy()
    
    # Filter by category if hints detected
    if category_hints:
        category_map = {
            "phone": "Phones",
            "laptop": "Laptops",
            "headphones": "Headphones",
            "smartwatch": "Smartwatches",
            "tablet": "Tablets",
            "accessories": "Accessories",
        }
        target_categories = [category_map.get(c) for c in category_hints if c in category_map]
        
        filtered = [p for p in candidates if p["category"] in target_categories]
        if filtered:
            candidates = filtered
    
    # Soft filter by budget (don't exclude, but prefer under budget)
    if budget:
        under_budget = [p for p in candidates if p["price"] <= budget]
        if under_budget:
            # Prefer under budget but keep some over-budget if needed
            slightly_over = [p for p in candidates if budget < p["price"] <= budget * 1.2]
            candidates = under_budget + slightly_over[:2]
    
    # Score all candidates
    scored_products = []
    for product in candidates:
        text_score = calculate_text_match_score(product, query)
        budget_score = calculate_budget_score(product, budget)
        quality_score = calculate_quality_score(product)
        
        total_score = text_score + budget_score + quality_score
        scored_products.append((product, total_score, text_score, budget_score))
    
    # Sort by total score descending
    scored_products.sort(key=lambda x: x[1], reverse=True)
    
    # Build recommendations with explanations
    recommendations = []
    for product, total_score, text_score, budget_score in scored_products[:max_results]:
        reasons = []
        
        # Budget reason
        if budget and product["price"] <= budget:
            savings = budget - product["price"]
            if savings > 0:
                reasons.append(f"${savings} under your ${budget} budget")
            else:
                reasons.append(f"Right at your ${budget} budget")
        
        # Quality reason
        if product["rating"] >= 4.5:
            reasons.append(f"Highly rated at {product['rating']}★")
        elif product["rating"] >= 4.0:
            reasons.append(f"Well-reviewed ({product['rating']}★)")
        
        # Feature matching reason
        matching_tags = [t for t in product.get("tags", []) if t.lower() in query.lower()]
        if matching_tags:
            reasons.append(f"Matches: {', '.join(matching_tags[:2])}")
        
        # Best-for reason as fallback
        if not reasons and product.get("best_for"):
            reasons.append(product["best_for"])
        
        # Ensure at least one reason
        if not reasons:
            reasons.append("Good match for your requirements")
        
        # Normalize score to 0-100 range
        # Typical scores range from -20 to 150, normalize to 30-95
        normalized_score = min(95, max(30, 30 + (total_score / 150) * 65))
        
        recommendations.append(RecommendationItem(
            product_id=product["id"],
            match_score=round(normalized_score, 1),
            reason=". ".join(reasons[:2])
        ))
    
    # Generate summary
    if recommendations:
        if budget:
            summary = f"Found {len(recommendations)} products matching your criteria within ${budget} budget using smart matching."
        else:
            summary = f"Found {len(recommendations)} products matching your criteria using smart matching."
    else:
        summary = "No products found matching your criteria. Try broadening your search."
    
    logger.info(f"Fallback engine returned {len(recommendations)} recommendations")
    
    return RecommendationResponse(
        recommendations=recommendations,
        summary=summary,
        source="fallback"
    )
