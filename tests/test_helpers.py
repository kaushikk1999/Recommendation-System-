"""
Unit Tests for Helper Functions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


class TestValidateQuery:
    """Tests for query validation."""
    
    def test_valid_query(self):
        from app.utils.helpers import validate_query
        
        is_valid, error = validate_query("phone under $500")
        assert is_valid is True
        assert error == ""
    
    def test_empty_query(self):
        from app.utils.helpers import validate_query
        
        is_valid, error = validate_query("")
        assert is_valid is False
        assert "enter" in error.lower()
    
    def test_short_query(self):
        from app.utils.helpers import validate_query
        
        is_valid, error = validate_query("ab")
        assert is_valid is False
        assert "short" in error.lower()
    
    def test_xss_prevention(self):
        from app.utils.helpers import validate_query
        
        is_valid, error = validate_query("<script>alert('xss')</script>")
        assert is_valid is False


class TestSanitizeQuery:
    """Tests for query sanitization."""
    
    def test_removes_html_tags(self):
        from app.utils.helpers import sanitize_query
        
        result = sanitize_query("<b>phone</b>")
        assert "<" not in result
        assert ">" not in result
    
    def test_normalizes_whitespace(self):
        from app.utils.helpers import sanitize_query
        
        result = sanitize_query("phone    under     $500")
        assert "    " not in result
    
    def test_strips_input(self):
        from app.utils.helpers import sanitize_query
        
        result = sanitize_query("  phone  ")
        assert result == "phone"
    
    def test_truncates_long_input(self):
        from app.utils.helpers import sanitize_query
        
        long_input = "a" * 1000
        result = sanitize_query(long_input)
        assert len(result) <= 500


class TestProductData:
    """Tests for product data integrity."""
    
    def test_all_products_have_required_fields(self):
        from app.data.products import get_all_products
        
        products = get_all_products()
        required_fields = ["id", "name", "category", "price", "rating", "description", "specs", "tags"]
        
        for product in products:
            for field in required_fields:
                assert field in product, f"Product {product.get('name', 'unknown')} missing {field}"
    
    def test_product_ids_unique(self):
        from app.data.products import get_all_products
        
        products = get_all_products()
        ids = [p["id"] for p in products]
        assert len(ids) == len(set(ids)), "Duplicate product IDs found"
    
    def test_get_product_by_id_found(self):
        from app.data.products import get_product_by_id
        
        product = get_product_by_id("phone-001")
        assert product is not None
        assert product["name"] == "Pixel Nova X1"
    
    def test_get_product_by_id_not_found(self):
        from app.data.products import get_product_by_id
        
        product = get_product_by_id("nonexistent-id")
        assert product is None
    
    def test_all_categories_present(self):
        from app.data.products import get_all_products, get_all_categories
        
        categories = get_all_categories()
        expected = ["Phones", "Laptops", "Headphones", "Smartwatches", "Tablets", "Accessories"]
        
        for cat in expected:
            assert cat in categories


class TestPydanticModels:
    """Tests for Pydantic model validation."""
    
    def test_recommendation_item_valid(self):
        from app.api.schemas import RecommendationItem
        
        item = RecommendationItem(
            product_id="phone-001",
            match_score=85.5,
            reason="Great match"
        )
        assert item.product_id == "phone-001"
        assert item.match_score == 85.5
    
    def test_recommendation_item_score_clamped(self):
        from app.api.schemas import RecommendationItem
        
        # Score should be rounded
        item = RecommendationItem(
            product_id="phone-001",
            match_score=85.567,
            reason="Great match"
        )
        assert item.match_score == 85.6
    
    def test_user_query_sanitization(self):
        from app.api.schemas import UserQuery
        
        query = UserQuery(
            text="  phone under $500  ",
            category_filter="Phones",
            max_budget=500
        )
        assert query.text == "phone under $500"
    
    def test_recommendation_response_valid(self):
        from app.api.schemas import RecommendationResponse, RecommendationItem
        
        response = RecommendationResponse(
            recommendations=[
                RecommendationItem(
                    product_id="phone-001",
                    match_score=90,
                    reason="Perfect match"
                )
            ],
            summary="Found 1 product",
            source="fallback"
        )
        assert len(response.recommendations) == 1
        assert response.source == "fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
