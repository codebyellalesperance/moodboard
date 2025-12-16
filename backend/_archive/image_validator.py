import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


def validate_image_url(url, min_size_kb=10, timeout=3):
    """
    Validate that an image URL:
    - Returns HTTP 200
    - Has image content-type
    - Meets minimum file size (filters tiny placeholders)

    Args:
        url: Image URL to validate
        min_size_kb: Minimum file size in KB (default 10KB)
        timeout: Request timeout in seconds

    Returns:
        bool: True if image is valid
    """
    if not url or not url.startswith('http'):
        return False

    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)

        if response.status_code != 200:
            return False

        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return False

        # Check Content-Length to filter tiny placeholder images
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) < min_size_kb * 1024:
            return False

        return True
    except Exception as e:
        logger.debug(f"Image validation failed for {url}: {e}")
        return False


def filter_valid_products(products, max_workers=10):
    """
    Filter products to only those with valid images.
    Uses ThreadPoolExecutor for parallel validation.

    Args:
        products: List of product dicts with 'image_url' field
        max_workers: Number of parallel validation threads

    Returns:
        List of products with valid images
    """
    if not products:
        return []

    valid_products = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all validation tasks
        future_to_product = {
            executor.submit(validate_image_url, p.get('image_url')): p
            for p in products
        }

        # Collect results as they complete
        for future in as_completed(future_to_product):
            product = future_to_product[future]
            try:
                if future.result():
                    valid_products.append(product)
            except Exception:
                pass  # Skip products that fail validation

    return valid_products
