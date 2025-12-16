import requests
import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

SHOPSTYLE_BASE_URL = "https://api.shopstyle.com/api/v2"


def search_products(
    query: str,
    num_results: int = 10,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None
) -> List[Dict]:
    """
    Search ShopStyle Collective API for products.

    Args:
        query: Search query string
        num_results: Number of results to return (max 50)
        min_price: Minimum price filter
        max_price: Maximum price filter

    Returns:
        List of product dicts with affiliate links
    """

    url = f"{SHOPSTYLE_BASE_URL}/products"

    params = {
        "pid": Config.SHOPSTYLE_PID,
        "fts": query,
        "offset": 0,
        "limit": min(num_results, 50),
        "sort": "Popular"
    }

    # Add price filters
    if min_price is not None or max_price is not None:
        min_p = min_price or 0
        max_p = max_price or 10000
        params["fl"] = f"p:{min_p}:{max_p}"

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"ShopStyle API error: {e}")
        return []

    products = []

    for item in data.get("products", []):
        product = format_product(item, query)
        if product:
            products.append(product)

    return products


def format_product(item: dict, query: str) -> Optional[Dict]:
    """
    Format a ShopStyle product into our standard format.

    Args:
        item: Raw product data from ShopStyle
        query: The search query that found this product

    Returns:
        Formatted product dict or None if invalid
    """

    try:
        # Get the best available image
        image_url = ""
        image_sizes = item.get("image", {}).get("sizes", {})
        for size in ["Large", "Medium", "Small", "Original"]:
            if size in image_sizes:
                image_url = image_sizes[size].get("url", "")
                break

        # Get prices
        price = item.get("salePrice") or item.get("price") or 0
        original_price = item.get("price") or price

        return {
            "id": f"ss_{item.get('id', '')}",
            "name": item.get("name", "Unknown Product"),
            "brand": item.get("brand", {}).get("name", ""),
            "price": round(float(price), 2),
            "original_price": round(float(original_price), 2),
            "on_sale": float(price) < float(original_price),
            "currency": "USD",
            "image_url": image_url,
            "product_url": item.get("clickUrl", ""),  # Affiliate link!
            "retailer": item.get("retailer", {}).get("name", ""),
            "category": item.get("categories", [{}])[0].get("name", "") if item.get("categories") else "",
            "match_reason": query,
            "in_stock": item.get("inStock", True)
        }
    except Exception as e:
        print(f"Error formatting product: {e}")
        return None


def search_all_queries(
    search_queries: List[str],
    max_products: int = 20,
    budget: Optional[str] = None
) -> List[Dict]:
    """
    Search multiple queries and combine/dedupe results.

    Args:
        search_queries: List of search query strings
        max_products: Maximum total products to return
        budget: Optional budget hint ("affordable", "mid-range", "luxury")

    Returns:
        Deduped list of products
    """

    all_products = []
    seen_ids = set()

    # Set price filters based on budget
    min_price, max_price = None, None
    if budget == "affordable":
        max_price = 75
    elif budget == "mid-range":
        min_price = 50
        max_price = 200
    elif budget == "luxury":
        min_price = 150

    # Over-fetch to account for invalid images being filtered out
    fetch_target = int(max_products * 1.5)

    # Use up to 8 queries
    queries_to_use = search_queries[:8]
    products_per_query = max(3, fetch_target // len(queries_to_use)) if queries_to_use else 0

    for query in queries_to_use:
        try:
            products = search_products(
                query=query,
                num_results=products_per_query,
                min_price=min_price,
                max_price=max_price
            )

            for product in products:
                # Dedupe by product ID
                if product["id"] not in seen_ids:
                    seen_ids.add(product["id"])
                    all_products.append(product)

        except Exception as e:
            logger.error(f"Error searching '{query}': {e}")
            continue

    # Skip image validation - ShopStyle images are generally reliable
    # and many CDNs block HEAD requests causing false negatives
    validated_products = all_products
    logger.info(f"Fetched {len(validated_products)} products")

    # Sort: in-stock first, then sale items, then by price
    validated_products.sort(key=lambda x: (
        not x.get("in_stock", True),
        not x.get("on_sale", False),
        x.get("price", 0)
    ))

    return validated_products[:max_products]


def detect_budget_from_prompt(prompt: str) -> Optional[str]:
    """
    Detect budget hints from user prompt.

    Args:
        prompt: User's prompt string

    Returns:
        Budget category or None
    """
    prompt_lower = prompt.lower()

    affordable_keywords = ['affordable', 'cheap', 'budget', 'under $50', 'under $75', 'under $100', 'inexpensive', 'low cost']
    luxury_keywords = ['luxury', 'designer', 'high-end', 'expensive', 'premium', 'splurge']

    for keyword in affordable_keywords:
        if keyword in prompt_lower:
            return "affordable"

    for keyword in luxury_keywords:
        if keyword in prompt_lower:
            return "luxury"

    return None
