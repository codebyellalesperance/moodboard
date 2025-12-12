"""ShopStyle Collective API integration for product search."""

import requests
from config import Config

SHOPSTYLE_API_URL = 'https://api.shopstyle.com/api/v2/products'


def search_products(mood_result: dict, limit_per_query: int = 4) -> list[dict]:
    """
    Search ShopStyle for products matching the mood profile.

    Args:
        mood_result: Mood profile from vision service
        limit_per_query: Max products per search query

    Returns:
        List of product dicts with id, name, brand, price, image_url, product_url, etc.
    """
    search_queries = mood_result.get('search_queries', [])
    all_products = []
    seen_ids = set()

    for query in search_queries:
        try:
            response = requests.get(
                SHOPSTYLE_API_URL,
                params={
                    'pid': Config.SHOPSTYLE_PID,
                    'fts': query,
                    'limit': limit_per_query,
                    'sort': 'Popular'
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            for product in data.get('products', []):
                product_id = str(product.get('id'))

                # Skip duplicates
                if product_id in seen_ids:
                    continue
                seen_ids.add(product_id)

                all_products.append(format_product(product, query))

        except requests.RequestException as e:
            # Log but continue with other queries
            print(f'ShopStyle error for query "{query}": {e}')
            continue

    return all_products


def format_product(product: dict, match_reason: str) -> dict:
    """Format a ShopStyle product for the API response."""
    price_info = product.get('priceLabel', '')
    sale_price = product.get('salePrice')
    original_price = product.get('price')

    return {
        'id': f"ss_{product.get('id')}",
        'name': product.get('name', ''),
        'brand': product.get('brand', {}).get('name', ''),
        'price': sale_price or original_price,
        'original_price': original_price if sale_price else None,
        'on_sale': sale_price is not None and sale_price < original_price,
        'currency': 'USD',
        'image_url': product.get('image', {}).get('sizes', {}).get('Large', {}).get('url', ''),
        'product_url': product.get('clickUrl', ''),  # Affiliate link
        'retailer': product.get('retailer', {}).get('name', ''),
        'category': product.get('categories', [{}])[0].get('name', '') if product.get('categories') else '',
        'match_reason': match_reason,
        'in_stock': product.get('inStock', True)
    }
