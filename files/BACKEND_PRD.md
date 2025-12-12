# Backend PRD: Moodboard — Shop the Aesthetic, Not the Item

## Overview

**Product Name:** Moodboard

**Backend Purpose:** Receive images and an optional prompt from the frontend, extract aesthetic/mood information using a vision AI model, query shopping APIs for matching products, and return structured results.

**Core Flow:**
```
Images + Prompt → Vision AI (mood extraction) → Shopping API (product search) → Structured Response
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT                                      │
│                         (React Frontend)                                 │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  │ POST /api/moodcheck
                                  │ { images: [base64...], prompt: "..." }
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BACKEND SERVER                                   │
│                      (Flask / FastAPI / Node)                            │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                        /api/moodcheck                               │ │
│  │                                                                     │ │
│  │  1. Validate request (images, prompt)                              │ │
│  │  2. Send images to Vision API                                       │ │
│  │  3. Parse mood profile from AI response                            │ │
│  │  4. Generate search queries from mood profile                      │ │
│  │  5. Query Shopping API for each search term                        │ │
│  │  6. Dedupe and rank products                                        │ │
│  │  7. Return structured response                                      │ │
│  │                                                                     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────┬──────────────────────────────┬───────────────────────┘
                   │                              │
                   ▼                              ▼
┌──────────────────────────────┐    ┌──────────────────────────────────────┐
│        VISION API            │    │          SHOPPING API                 │
│                              │    │                                       │
│  Options:                    │    │  Options:                             │
│  • OpenAI GPT-4V             │    │  • SerpApi Google Shopping            │
│  • Anthropic Claude Vision   │    │  • ShopStyle Collective               │
│  • Google Gemini Pro Vision  │    │  • Amazon Product API                 │
│                              │    │  • RapidAPI aggregators               │
└──────────────────────────────┘    └──────────────────────────────────────┘
```

---

## API Specification

### Endpoint: POST `/api/moodcheck`

**Description:** Analyze uploaded images to extract aesthetic vibe and return matching shoppable products.

#### Request

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "images": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..."
  ],
  "prompt": "This vibe but affordable and for summer"
}
```

**Field Specifications:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `images` | array[string] | Yes | 1-5 Base64 encoded images with data URI prefix |
| `prompt` | string | No | Optional modifier (max 200 chars). Empty string if not provided. |

**Validation Rules:**
- `images` must contain 1-5 items
- Each image must be valid Base64 with data URI prefix
- Each image must be < 5MB when decoded
- Supported formats: JPEG, PNG, WEBP
- `prompt` max length: 200 characters

#### Response (Success)

**Status:** `200 OK`

```json
{
  "success": true,
  "vibe": {
    "name": "Quiet Luxury Coastal",
    "mood": "Effortless, polished, understated confidence",
    "color_palette": [
      {"name": "Cream", "hex": "#F5F5DC"},
      {"name": "Camel", "hex": "#C19A6B"},
      {"name": "White", "hex": "#FFFFFF"},
      {"name": "Soft Grey", "hex": "#D3D3D3"},
      {"name": "Navy", "hex": "#000080"}
    ],
    "textures": ["linen", "cashmere", "cotton", "silk", "light knit"],
    "key_pieces": [
      "Oversized neutral blazer",
      "White tank bodysuit",
      "High-waisted tailored trousers",
      "Minimal gold jewelry",
      "Clean white sneakers",
      "Structured tote bag"
    ],
    "avoid": ["Loud logos", "neon colors", "distressed denim", "chunky sneakers"]
  },
  "products": [
    {
      "id": "ss_1234567890",
      "name": "Oversized Linen Blazer",
      "brand": "Vince",
      "price": 89.99,
      "original_price": 145.00,
      "on_sale": true,
      "currency": "USD",
      "image_url": "https://img.shopstyle-cdn.com/...",
      "product_url": "https://api.shopstyle.com/action/apiVisitRetailer?id=...",
      "retailer": "Nordstrom",
      "category": "Jackets",
      "match_reason": "Oversized neutral blazer",
      "colors": ["Cream", "Beige"],
      "in_stock": true
    },
    {
      "id": "ss_0987654321",
      "name": "Ribbed Cotton Tank Bodysuit",
      "brand": "Everlane",
      "price": 28.00,
      "original_price": 28.00,
      "on_sale": false,
      "currency": "USD",
      "image_url": "https://img.shopstyle-cdn.com/...",
      "product_url": "https://api.shopstyle.com/action/apiVisitRetailer?id=...",
      "retailer": "Everlane",
      "category": "Tops",
      "match_reason": "White tank bodysuit",
      "colors": ["White"],
      "in_stock": true
    }
  ],
  "search_queries_used": [
    "cream oversized linen blazer women",
    "white ribbed tank bodysuit",
    "camel wide leg trousers women"
  ]
}
```

#### Response (Error)

**Status:** `400 Bad Request` (validation error)
```json
{
  "success": false,
  "error": "Invalid request",
  "details": "At least one image is required"
}
```

**Status:** `500 Internal Server Error` (processing error)
```json
{
  "success": false,
  "error": "Unable to analyze images. Please try again."
}
```

**Status:** `503 Service Unavailable` (API dependency down)
```json
{
  "success": false,
  "error": "Service temporarily unavailable. Please try again in a few minutes."
}
```

---

## Core Logic

### Step 1: Request Validation

```python
def validate_request(data):
    errors = []
    
    # Check images exist
    if 'images' not in data or not data['images']:
        errors.append("At least one image is required")
    
    # Check image count
    if len(data.get('images', [])) > 5:
        errors.append("Maximum 5 images allowed")
    
    # Validate each image
    for i, img in enumerate(data.get('images', [])):
        if not img.startswith('data:image/'):
            errors.append(f"Image {i+1} is not a valid data URI")
        
        # Check format
        if not any(img.startswith(f'data:image/{fmt}') for fmt in ['jpeg', 'png', 'webp']):
            errors.append(f"Image {i+1} must be JPEG, PNG, or WEBP")
        
        # Check size (rough estimate from base64 length)
        base64_data = img.split(',')[1] if ',' in img else img
        estimated_size = len(base64_data) * 0.75  # Base64 is ~33% larger
        if estimated_size > 5 * 1024 * 1024:  # 5MB
            errors.append(f"Image {i+1} exceeds 5MB limit")
    
    # Check prompt length
    if len(data.get('prompt', '')) > 200:
        errors.append("Prompt must be 200 characters or less")
    
    return errors
```

### Step 2: Vision API Integration

**Primary Choice: OpenAI GPT-4V**

```python
import openai
import base64
import json

MOOD_EXTRACTION_PROMPT = """
Analyze these images together as a single mood board. The user wants to shop this vibe.

User's request: {user_prompt}

Your task: Extract the AESTHETIC ESSENCE — not what's literally in the image, but the FEELING and STYLE ENERGY someone would want to recreate through clothing and accessories.

Return a JSON object with exactly these fields:

{{
  "name": "A catchy 2-5 word aesthetic name (e.g., 'Coastal Grandmother', 'Old Money Tennis', '90s Minimalist', 'Dark Academia')",
  
  "mood": "2-4 words describing the emotional energy (e.g., 'Effortless, polished, confident')",
  
  "color_palette": [
    {{"name": "Color name", "hex": "#HEXCODE"}},
    // 4-6 colors that define this vibe. Be specific: "warm camel" not just "brown"
  ],
  
  "textures": ["texture1", "texture2", "texture3"],
  // 4-6 fabrics/materials that belong in this vibe
  
  "key_pieces": [
    "Specific item 1",
    "Specific item 2"
  ],
  // 5-7 specific clothing/accessory items that capture this vibe
  // Be specific enough to search: "oversized linen blazer" not just "blazer"
  
  "avoid": ["thing1", "thing2"],
  // 3-5 things that do NOT fit this vibe
  
  "search_queries": [
    "specific searchable product query 1",
    "specific searchable product query 2"
  ]
  // 8-12 specific product search terms that would return items matching this vibe
  // These should be real queries someone could type into a shopping site
  // Include descriptors: "cream linen wide leg pants women" not "pants"
  // If user mentioned budget constraints, include "affordable" or "under $X" in some queries
}}

Important:
- If the user's prompt modifies the vibe (e.g., "but affordable", "but for summer", "work appropriate"), adjust ALL your recommendations accordingly
- Focus on the FEELING, not literal items in the image
- Be specific enough that search results will be relevant
- Return ONLY valid JSON, no other text
"""

def extract_mood(images: list, prompt: str) -> dict:
    """
    Send images to GPT-4V and extract mood profile.
    
    Args:
        images: List of base64 encoded images with data URI prefix
        prompt: User's optional modifier prompt
        
    Returns:
        Parsed mood profile dict
    """
    
    # Build message content with images
    content = []
    
    # Add each image
    for img in images:
        # Extract base64 data and media type
        media_type = img.split(';')[0].split(':')[1]  # e.g., "image/jpeg"
        base64_data = img.split(',')[1]
        
        content.append({
            "type": "image_url",
            "image_url": {
                "url": img,
                "detail": "high"
            }
        })
    
    # Add the prompt
    formatted_prompt = VIBE_EXTRACTION_PROMPT.format(
        user_prompt=prompt if prompt else "No specific modifications requested"
    )
    content.append({
        "type": "text",
        "text": formatted_prompt
    })
    
    # Call GPT-4V
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=2000,
        temperature=0.7
    )
    
    # Parse JSON from response
    response_text = response.choices[0].message.content
    
    # Clean up response (sometimes GPT adds markdown code blocks)
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]
    
    mood_profile = json.loads(response_text.strip())
    
    return mood_profile
```

**Alternative: Anthropic Claude Vision**

```python
import anthropic
import json

def extract_mood_claude(images: list, prompt: str) -> dict:
    """
    Send images to Claude Vision and extract mood profile.
    """
    
    client = anthropic.Anthropic()
    
    # Build content with images
    content = []
    
    for img in images:
        media_type = img.split(';')[0].split(':')[1]
        base64_data = img.split(',')[1]
        
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64_data
            }
        })
    
    formatted_prompt = VIBE_EXTRACTION_PROMPT.format(
        user_prompt=prompt if prompt else "No specific modifications requested"
    )
    content.append({
        "type": "text",
        "text": formatted_prompt
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    
    response_text = response.content[0].text
    
    # Parse JSON
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    
    return json.loads(response_text.strip())
```

### Step 3: Shopping API Integration

**Primary Choice: ShopStyle Collective API**

ShopStyle Collective is ideal for this app because:
- Fashion-focused inventory (not random products)
- Affiliate links built into every `clickUrl` (you earn commission)
- Filters for category, brand, price, color, size
- Free with partner account
- 1000+ retailers including Nordstrom, ASOS, Revolve, Shopbop, etc.

```python
import requests
from typing import List, Dict, Optional

SHOPSTYLE_PID = "your_partner_id"  # Your ShopStyle Collective partner ID
SHOPSTYLE_BASE_URL = "https://api.shopstyle.com/api/v2"

def search_products(
    query: str, 
    num_results: int = 10,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    category: Optional[str] = None
) -> List[Dict]:
    """
    Search ShopStyle Collective API for products matching the query.
    
    Args:
        query: Search query string (e.g., "cream linen blazer women")
        num_results: Number of results to return (max 50 per request)
        min_price: Minimum price filter in dollars
        max_price: Maximum price filter in dollars
        category: Category filter (e.g., "womens-clothes", "womens-shoes")
        
    Returns:
        List of product dicts with affiliate links
    """
    
    url = f"{SHOPSTYLE_BASE_URL}/products"
    
    params = {
        "pid": SHOPSTYLE_PID,
        "fts": query,           # Full text search
        "offset": 0,
        "limit": min(num_results, 50),  # API max is 50
        "sort": "Popular"       # Options: Popular, PriceLoHi, PriceHiLo, Recency
    }
    
    # Add optional filters
    if min_price:
        params["fl"] = f"p:{min_price}:{max_price or 10000}"
    elif max_price:
        params["fl"] = f"p:0:{max_price}"
    
    if category:
        params["cat"] = category
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"ShopStyle API error: {e}")
        return []
    
    products = []
    
    for item in data.get("products", []):
        # Extract the best image size available
        image_url = ""
        image_sizes = item.get("image", {}).get("sizes", {})
        for size in ["Large", "Medium", "Small", "Original"]:
            if size in image_sizes:
                image_url = image_sizes[size].get("url", "")
                break
        
        # Extract price (handle sale prices)
        price = item.get("salePrice") or item.get("price") or 0
        original_price = item.get("price", price)
        
        products.append({
            "id": f"ss_{item.get('id', '')}",
            "name": item.get("name", ""),
            "brand": item.get("brand", {}).get("name", ""),
            "price": price,
            "original_price": original_price,
            "on_sale": price < original_price,
            "currency": "USD",
            "image_url": image_url,
            "product_url": item.get("clickUrl", ""),  # This is your affiliate link!
            "retailer": item.get("retailer", {}).get("name", ""),
            "category": item.get("categories", [{}])[0].get("name", "") if item.get("categories") else "",
            "match_reason": query,
            "colors": [c.get("name") for c in item.get("colors", [])],
            "in_stock": item.get("inStock", True)
        })
    
    return products


def search_by_color(color_hex: str, category: str = "womens-clothes", num_results: int = 10) -> List[Dict]:
    """
    Search for products by color.
    
    ShopStyle supports color filtering which is perfect for vibe matching.
    """
    
    # Map common color names to ShopStyle color filters
    color_map = {
        "cream": "Beige",
        "camel": "Brown",
        "navy": "Blue",
        "burgundy": "Red",
        "olive": "Green",
        "blush": "Pink",
        "charcoal": "Gray",
        "ivory": "White",
        "cognac": "Brown",
        "tan": "Brown",
        "rust": "Orange"
    }
    
    url = f"{SHOPSTYLE_BASE_URL}/products"
    
    params = {
        "pid": SHOPSTYLE_PID,
        "cat": category,
        "offset": 0,
        "limit": num_results,
        "sort": "Popular"
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    return [format_product(item) for item in data.get("products", [])]


def search_all_queries(
    search_queries: List[str], 
    max_products: int = 20,
    budget: Optional[str] = None
) -> List[Dict]:
    """
    Search multiple queries and combine/dedupe results.
    
    Args:
        search_queries: List of search query strings from mood extraction
        max_products: Maximum total products to return
        budget: Optional budget hint ("affordable", "luxury", "mid-range")
        
    Returns:
        Deduped list of products sorted by relevance
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
    
    # Use up to 8 queries to avoid rate limits
    queries_to_use = search_queries[:8]
    products_per_query = max(3, max_products // len(queries_to_use))
    
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
            print(f"Error searching '{query}': {e}")
            continue
    
    # Sort by: in-stock first, then by sale items, then by price
    all_products.sort(key=lambda x: (
        not x.get("in_stock", True),  # In-stock first
        not x.get("on_sale", False),   # Sale items second
        x.get("price", 0)              # Then by price
    ))
    
    return all_products[:max_products]


def get_categories() -> List[Dict]:
    """
    Get available ShopStyle categories for filtering.
    Useful for letting users narrow down results.
    """
    
    url = f"{SHOPSTYLE_BASE_URL}/categories"
    params = {"pid": SHOPSTYLE_PID}
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    return data.get("categories", [])


def get_brands(prefix: str = "") -> List[Dict]:
    """
    Get available brands, optionally filtered by prefix.
    """
    
    url = f"{SHOPSTYLE_BASE_URL}/brands"
    params = {
        "pid": SHOPSTYLE_PID,
        "prefix": prefix
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    return data.get("brands", [])


def get_retailers() -> List[Dict]:
    """
    Get list of retailers in ShopStyle network.
    Includes Nordstrom, ASOS, Revolve, Shopbop, Saks, Net-a-Porter, etc.
    """
    
    url = f"{SHOPSTYLE_BASE_URL}/retailers"
    params = {"pid": SHOPSTYLE_PID}
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    return data.get("retailers", [])
```

### ShopStyle Category Reference

Common categories for the `cat` parameter:

```python
SHOPSTYLE_CATEGORIES = {
    # Women's
    "womens-clothes": "All Women's Clothing",
    "womens-tops": "Tops",
    "womens-dresses": "Dresses", 
    "womens-pants": "Pants",
    "womens-jeans": "Jeans",
    "womens-skirts": "Skirts",
    "womens-shorts": "Shorts",
    "womens-jackets-and-coats": "Jackets & Coats",
    "womens-sweaters": "Sweaters",
    "womens-shoes": "Shoes",
    "womens-bags": "Bags",
    "womens-jewelry": "Jewelry",
    "womens-accessories": "Accessories",
    "womens-swimwear": "Swimwear",
    
    # Men's
    "mens-clothes": "All Men's Clothing",
    "mens-shirts": "Shirts",
    "mens-pants": "Pants",
    "mens-shoes": "Shoes",
    "mens-accessories": "Accessories",
}
```

### Price Filter Examples

```python
# Affordable (under $75)
params["fl"] = "p:0:75"

# Mid-range ($50-$200)
params["fl"] = "p:50:200"

# Luxury ($200+)
params["fl"] = "p:200:10000"

# Multiple filters (price AND on sale)
params["fl"] = ["p:0:100", "s:Sale"]
```

### Step 4: Main Endpoint Handler

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/api/moodcheck', methods=['POST'])
def moodcheck():
    """
    Main endpoint: Analyze images and return vibe + products.
    """
    
    try:
        data = request.get_json()
        
        # Step 1: Validate request
        validation_errors = validate_request(data)
        if validation_errors:
            return jsonify({
                "success": False,
                "error": "Invalid request",
                "details": validation_errors
            }), 400
        
        images = data.get('images', [])
        prompt = data.get('prompt', '')
        
        # Step 2: Extract vibe from images
        try:
            mood_profile = extract_mood(images, prompt)
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "error": "Unable to analyze images. Please try different images."
            }), 500
        except Exception as e:
            print(f"Vision API error: {e}")
            return jsonify({
                "success": False,
                "error": "Unable to analyze images. Please try again."
            }), 500
        
        # Step 3: Search for products
        try:
            search_queries = mood_profile.get('search_queries', [])
            products = search_all_queries(search_queries, max_products=20)
        except Exception as e:
            print(f"Shopping API error: {e}")
            # Return vibe even if product search fails
            products = []
        
        # Step 4: Build response
        response = {
            "success": True,
            "vibe": {
                "name": mood_profile.get("name", "Your Vibe"),
                "mood": mood_profile.get("mood", ""),
                "color_palette": mood_profile.get("color_palette", []),
                "textures": mood_profile.get("textures", []),
                "key_pieces": mood_profile.get("key_pieces", []),
                "avoid": mood_profile.get("avoid", [])
            },
            "products": products,
            "search_queries_used": search_queries[:8]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Configuration & Environment

### Environment Variables

```bash
# .env file

# Vision API (choose one)
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Shopping API
SHOPSTYLE_PID=uid1234-12345678-90  # Your ShopStyle Collective Partner ID

# Server config
FLASK_ENV=development
PORT=5000

# Optional: Rate limiting
REDIS_URL=redis://localhost:6379
```

### Requirements

```txt
# requirements.txt

flask==3.0.0
flask-cors==4.0.0
openai==1.6.0
anthropic==0.8.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0  # For production
redis==5.0.0      # Optional: for rate limiting
```

---

## Error Handling

### Error Types & Responses

| Error Type | HTTP Status | Response |
|------------|-------------|----------|
| Missing images | 400 | `{"success": false, "error": "Invalid request", "details": "At least one image is required"}` |
| Too many images | 400 | `{"success": false, "error": "Invalid request", "details": "Maximum 5 images allowed"}` |
| Invalid image format | 400 | `{"success": false, "error": "Invalid request", "details": "Image must be JPEG, PNG, or WEBP"}` |
| Image too large | 400 | `{"success": false, "error": "Invalid request", "details": "Image exceeds 5MB limit"}` |
| Vision API failure | 500 | `{"success": false, "error": "Unable to analyze images. Please try again."}` |
| Vision API rate limit | 503 | `{"success": false, "error": "Service temporarily unavailable. Please try again in a few minutes."}` |
| Shopping API failure | 200 | Return vibe with empty products array |
| Unexpected error | 500 | `{"success": false, "error": "An unexpected error occurred. Please try again."}` |

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log key events
logger.info(f"Vibecheck request: {len(images)} images, prompt: '{prompt[:50]}...'")
logger.info(f"Vibe extracted: {mood_profile.get('name')}")
logger.info(f"Products found: {len(products)}")
logger.error(f"Vision API error: {e}")
```

---

## Rate Limiting & Caching

### Rate Limiting (Optional but Recommended)

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per minute"],
    storage_uri="redis://localhost:6379"
)

@app.route('/api/moodcheck', methods=['POST'])
@limiter.limit("10 per minute")
def moodcheck():
    # ... endpoint logic
```

### Caching (Optional)

```python
import hashlib
import json
from functools import lru_cache

def get_cache_key(images: list, prompt: str) -> str:
    """Generate cache key from images and prompt."""
    content = json.dumps(sorted(images) + [prompt])
    return hashlib.md5(content.encode()).hexdigest()

# Simple in-memory cache (use Redis for production)
vibe_cache = {}

def get_cached_vibe(cache_key: str):
    return vibe_cache.get(cache_key)

def set_cached_vibe(cache_key: str, vibe: dict, ttl: int = 3600):
    vibe_cache[cache_key] = vibe
    # In production, use Redis with TTL
```

---

## Testing

### Unit Tests

```python
# test_moodcheck.py

import pytest
import json
from app import app, validate_request, extract_price

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_validate_request_no_images():
    errors = validate_request({})
    assert "At least one image is required" in errors

def test_validate_request_too_many_images():
    data = {"images": ["img"] * 6}
    errors = validate_request(data)
    assert "Maximum 5 images allowed" in errors

def test_extract_price_simple():
    assert extract_price("$89.99") == 89.99

def test_extract_price_range():
    assert extract_price("$89.99 - $129.99") == 89.99

def test_extract_price_empty():
    assert extract_price("") == 0.0

def test_moodcheck_no_body(client):
    response = client.post('/api/moodcheck', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] == False

def test_moodcheck_valid_request(client, mocker):
    # Mock the Vision API
    mocker.patch('app.extract_mood', return_value={
        "name": "Test Vibe",
        "mood": "Casual",
        "color_palette": [],
        "textures": [],
        "key_pieces": [],
        "avoid": [],
        "search_queries": ["test query"]
    })
    
    # Mock the Shopping API
    mocker.patch('app.search_all_queries', return_value=[])
    
    # Valid base64 image (1x1 transparent PNG)
    test_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    response = client.post('/api/moodcheck', json={
        "images": [test_image],
        "prompt": "test prompt"
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] == True
    assert data["vibe"]["name"] == "Test Vibe"
```

### Manual Testing

```bash
# Test with curl

curl -X POST http://localhost:5000/api/moodcheck \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="],
    "prompt": "coastal summer vibe"
  }'
```

---

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=sk-...
export SERPAPI_KEY=...

# Run server
python app.py
# OR
flask run --port 5000
```

### Production (Render / Railway / Fly.io)

```bash
# Procfile
web: gunicorn app:app --workers 2 --timeout 120
```

```yaml
# render.yaml
services:
  - type: web
    name: vibe-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --workers 2 --timeout 120
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: SERPAPI_KEY
        sync: false
```

---

## File Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example           # Example env file
├── Procfile              # For Heroku/Render deployment
├── config.py             # Configuration management
├── services/
│   ├── __init__.py
│   ├── vision.py         # Vision API integration
│   └── shopping.py       # Shopping API integration
├── utils/
│   ├── __init__.py
│   ├── validation.py     # Request validation
│   └── helpers.py        # Helper functions
└── tests/
    ├── __init__.py
    ├── test_app.py
    ├── test_vision.py
    └── test_shopping.py
```

---

## Development Phases

### Phase 1: Basic Setup (1 hour)
- [ ] Set up Flask project structure
- [ ] Create `/api/moodcheck` endpoint skeleton
- [ ] Add request validation
- [ ] Return dummy response

### Phase 2: Vision API Integration (1-2 hours)
- [ ] Set up OpenAI/Anthropic client
- [ ] Write mood extraction prompt
- [ ] Parse JSON response
- [ ] Handle errors gracefully

### Phase 3: Shopping API Integration (1-2 hours)
- [ ] Set up SerpApi client
- [ ] Implement product search
- [ ] Add deduplication logic
- [ ] Combine results from multiple queries

### Phase 4: Polish (1 hour)
- [ ] Add logging
- [ ] Improve error messages
- [ ] Add CORS configuration
- [ ] Test end-to-end with frontend

### Phase 5: Deploy (30 min)
- [ ] Set up hosting (Render/Railway)
- [ ] Configure environment variables
- [ ] Test production endpoint

---

## Cost Estimates

| Service | Cost | Notes |
|---------|------|-------|
| OpenAI GPT-4V | ~$0.03-0.10 per request | Depends on image count/size |
| ShopStyle Collective | FREE | Unlimited API calls with partner account |
| Hosting (Render) | Free tier or $7/mo | |

**Per moodcheck cost:** ~$0.03-0.10 (Vision API only — ShopStyle is free!)

**Revenue potential:** ShopStyle affiliate links earn 5-20% commission on purchases. If 10% of users buy something averaging $75, you make $0.75-1.50 per moodcheck in affiliate revenue.

---

## Future Enhancements

1. **Caching:** Cache mood profiles and product searches in Redis
2. **Multiple shopping sources:** Combine SerpApi, ShopStyle, and Amazon
3. **Price filtering:** Add min/max price parameters
4. **Category filtering:** Let users specify clothing categories
5. **Affiliate links:** Integrate with affiliate networks for monetization
6. **Image URL input:** Accept URLs instead of just base64 uploads
7. **Webhook/async:** For long-running requests, use background jobs
