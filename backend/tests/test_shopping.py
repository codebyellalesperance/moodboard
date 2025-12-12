import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.shopping import format_product, detect_budget_from_prompt, search_all_queries

class TestFormatProduct:

    def test_format_valid_product(self):
        raw_product = {
            "id": "12345",
            "name": "Test Blazer",
            "brand": {"name": "TestBrand"},
            "price": 100.00,
            "salePrice": 75.00,
            "image": {
                "sizes": {
                    "Large": {"url": "https://example.com/large.jpg"},
                    "Small": {"url": "https://example.com/small.jpg"}
                }
            },
            "clickUrl": "https://api.shopstyle.com/action/...",
            "retailer": {"name": "Nordstrom"},
            "categories": [{"name": "Jackets"}],
            "inStock": True
        }

        result = format_product(raw_product, "test query")

        assert result["id"] == "ss_12345"
        assert result["name"] == "Test Blazer"
        assert result["brand"] == "TestBrand"
        assert result["price"] == 75.00
        assert result["original_price"] == 100.00
        assert result["on_sale"] is True
        assert result["image_url"] == "https://example.com/large.jpg"
        assert result["retailer"] == "Nordstrom"
        assert result["match_reason"] == "test query"

    def test_format_product_not_on_sale(self):
        raw_product = {
            "id": "12345",
            "name": "Test Item",
            "brand": {"name": "Brand"},
            "price": 100.00,
            "image": {"sizes": {}},
            "clickUrl": "https://example.com",
            "retailer": {"name": "Store"}
        }

        result = format_product(raw_product, "query")

        assert result["price"] == 100.00
        assert result["original_price"] == 100.00
        assert result["on_sale"] is False

    def test_format_product_missing_fields(self):
        raw_product = {
            "id": "12345",
            "name": "Minimal Product"
        }

        result = format_product(raw_product, "query")

        assert result["id"] == "ss_12345"
        assert result["name"] == "Minimal Product"
        assert result["brand"] == ""
        assert result["price"] == 0


class TestDetectBudget:

    def test_detect_affordable(self):
        assert detect_budget_from_prompt("I want something affordable") == "affordable"
        assert detect_budget_from_prompt("under $100 please") == "affordable"
        assert detect_budget_from_prompt("cheap options") == "affordable"

    def test_detect_luxury(self):
        assert detect_budget_from_prompt("luxury brands only") == "luxury"
        assert detect_budget_from_prompt("designer items") == "luxury"
        assert detect_budget_from_prompt("high-end fashion") == "luxury"

    def test_detect_none(self):
        assert detect_budget_from_prompt("summer vibes") is None
        assert detect_budget_from_prompt("casual outfit") is None
        assert detect_budget_from_prompt("") is None


class TestSearchAllQueries:

    def test_deduplication(self):
        """Test that duplicate products are removed."""
        # This is an integration test that requires API access
        # For unit testing, we'd mock the search_products function
        pass

    def test_empty_queries(self):
        result = search_all_queries([], max_products=20)
        assert result == []
