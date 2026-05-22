"""
Unit Tests for Fallback Recommendation Engine
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.fallback import (
    parse_budget_from_query,
    extract_category_hints,
    calculate_text_match_score,
    calculate_budget_score,
    fallback_recommend,
)
from app.data.products import get_all_products


class TestParseBudget:
    """Tests for budget parsing from natural language."""
    
    def test_under_pattern(self):
        assert parse_budget_from_query("phone under $500") == 500
        assert parse_budget_from_query("laptop under 1000") == 1000
    
    def test_below_pattern(self):
        assert parse_budget_from_query("tablet below $300") == 300
    
    def test_less_than_pattern(self):
        assert parse_budget_from_query("headphones less than $200") == 200
    
    def test_max_pattern(self):
        assert parse_budget_from_query("max $800 laptop") == 800
        assert parse_budget_from_query("maximum $600") == 600
    
    def test_budget_pattern(self):
        assert parse_budget_from_query("my budget is $400") == 400
        assert parse_budget_from_query("budget of 500") == 500
    
    def test_up_to_pattern(self):
        assert parse_budget_from_query("up to $700") == 700
    
    def test_no_budget(self):
        assert parse_budget_from_query("best phone for photography") is None
        assert parse_budget_from_query("lightweight laptop") is None


class TestCategoryExtraction:
    """Tests for category keyword extraction."""
    
    def test_phone_keywords(self):
        hints = extract_category_hints("I want a smartphone")
        assert "phone" in hints
        
        hints = extract_category_hints("best android phone")
        assert "phone" in hints
    
    def test_laptop_keywords(self):
        hints = extract_category_hints("need a notebook for school")
        assert "laptop" in hints
    
    def test_headphones_keywords(self):
        hints = extract_category_hints("wireless earbuds for workout")
        assert "headphones" in hints
    
    def test_smartwatch_keywords(self):
        hints = extract_category_hints("fitness tracker with GPS")
        assert "smartwatch" in hints
    
    def test_multiple_categories(self):
        hints = extract_category_hints("phone and laptop combo")
        assert "phone" in hints
        assert "laptop" in hints
    
    def test_no_category(self):
        hints = extract_category_hints("something good")
        assert len(hints) == 0


class TestTextMatchScore:
    """Tests for text matching score calculation."""
    
    def test_name_match_scores_high(self):
        product = {
            "name": "Pixel Nova X1",
            "description": "Great camera phone",
            "tags": ["photography"],
            "best_for": "Photography enthusiasts",
            "specs": {"camera": "50MP"}
        }
        score = calculate_text_match_score(product, "pixel phone")
        assert score > 0
    
    def test_tag_match_scores_high(self):
        product = {
            "name": "BassPods",
            "description": "Wireless headphones",
            "tags": ["long battery", "bass"],
            "best_for": "Music lovers",
            "specs": {"battery": "60h"}
        }
        score = calculate_text_match_score(product, "headphones with long battery")
        assert score > 0


class TestBudgetScore:
    """Tests for budget fit scoring."""
    
    def test_under_budget_positive(self):
        product = {"price": 400}
        score = calculate_budget_score(product, 500)
        assert score > 0
    
    def test_over_budget_negative(self):
        product = {"price": 600}
        score = calculate_budget_score(product, 500)
        assert score < 0
    
    def test_no_budget_zero(self):
        product = {"price": 500}
        score = calculate_budget_score(product, None)
        assert score == 0


class TestFallbackRecommend:
    """Integration tests for fallback recommendations."""
    
    def test_returns_recommendations(self):
        products = get_all_products()
        result = fallback_recommend("phone under $500", products)
        
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        assert result["source"] == "fallback"
    
    def test_respects_budget(self):
        products = get_all_products()
        result = fallback_recommend("phone under $300", products)
        
        for rec in result["recommendations"]:
            product = next(p for p in products if p["id"] == rec.product_id)
            # Should prefer products under budget
            assert product["price"] <= 400  # Some tolerance
    
    def test_respects_category(self):
        products = get_all_products()
        result = fallback_recommend("laptop for students", products)
        
        # At least one recommendation should be a laptop
        laptop_found = False
        for rec in result["recommendations"]:
            product = next(p for p in products if p["id"] == rec.product_id)
            if product["category"] == "Laptops":
                laptop_found = True
                break
        assert laptop_found
    
    def test_max_results_limit(self):
        products = get_all_products()
        result = fallback_recommend("any product", products, max_results=2)
        
        assert len(result["recommendations"]) <= 2
    
    def test_includes_summary(self):
        products = get_all_products()
        result = fallback_recommend("phone", products)
        
        assert "summary" in result
        assert len(result["summary"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
