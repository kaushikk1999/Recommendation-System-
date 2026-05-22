"""
Pydantic Models for Data Validation
Ensures type safety and data integrity throughout the application.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class ProductCategory(str, Enum):
    """Valid product categories."""
    PHONES = "Phones"
    LAPTOPS = "Laptops"
    HEADPHONES = "Headphones"
    SMARTWATCHES = "Smartwatches"
    TABLETS = "Tablets"
    ACCESSORIES = "Accessories"


class ProductSpecs(BaseModel):
    """Product specifications - flexible dict structure."""
    model_config = {"extra": "allow"}


class Product(BaseModel):
    """Product data model with validation."""
    id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    category: str
    price: float = Field(..., gt=0, le=100000)
    rating: float = Field(..., ge=0, le=5)
    description: str = Field(..., min_length=1, max_length=500)
    specs: dict
    tags: list[str] = Field(default_factory=list)
    emoji: str = Field(default="📦", max_length=10)
    best_for: str = Field(default="", max_length=200)

    @field_validator("rating")
    @classmethod
    def round_rating(cls, v: float) -> float:
        return round(v, 1)

    @field_validator("tags")
    @classmethod
    def lowercase_tags(cls, v: list[str]) -> list[str]:
        return [tag.lower().strip() for tag in v]


class RecommendationItem(BaseModel):
    """Single recommendation item."""
    product_id: str = Field(..., min_length=1)
    match_score: float = Field(..., ge=0, le=100)
    reason: str = Field(..., min_length=1, max_length=500)

    @field_validator("match_score")
    @classmethod
    def round_score(cls, v: float) -> float:
        return round(v, 1)


class RecommendationResponse(BaseModel):
    """Full recommendation response from AI or fallback."""
    recommendations: list[RecommendationItem] = Field(default_factory=list)
    summary: str = Field(default="")
    source: str = Field(default="unknown")  # "ai" or "fallback"
    warning: Optional[str] = None

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        if v not in ("ai", "fallback", "unknown"):
            return "unknown"
        return v


class UserQuery(BaseModel):
    """Validated user input query."""
    text: str = Field(..., min_length=1, max_length=500)
    category_filter: Optional[str] = None
    max_budget: Optional[int] = Field(default=None, ge=0, le=100000)

    @field_validator("text")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        import html
        import re
        # HTML escape and remove potentially dangerous characters
        v = html.escape(v.strip())
        v = re.sub(r'[<>{}\\]', '', v)
        return v


class HealthStatus(BaseModel):
    """System health check response."""
    status: str = Field(default="healthy")
    api_configured: bool
    products_count: int
    cache_enabled: bool
    timestamp: str


class AnalyticsEvent(BaseModel):
    """Analytics event for tracking."""
    event_name: str
    properties: dict = Field(default_factory=dict)
    timestamp: str
    session_id: Optional[str] = None
