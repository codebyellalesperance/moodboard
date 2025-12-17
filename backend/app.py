from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from concurrent.futures import ThreadPoolExecutor
from config import Config
from utils.validation import validate_moodcheck_request
from utils.logger import logger
from services.vision import extract_mood
from services.shopping import search_all_queries, detect_budget_from_prompt, detect_item_type_from_prompt, filter_by_item_type
from services.trends import get_trend_summary
import time

# Validate config on startup
Config.validate()

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "20 per hour"],
    storage_uri="memory://"
)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'moodboard-api'
    })


@app.route('/api/trend/<keyword>', methods=['GET'])
@limiter.limit("30 per minute")
def get_trend(keyword):
    """
    Get trend data for an aesthetic/keyword.

    Returns:
        - direction: "rising" | "falling" | "stable" | "unknown"
        - change: percentage string like "+34%" or "-12%"
        - sparkline: list of values for mini chart
        - peak: when the trend peaked
        - current: current interest value (0-100)
    """
    logger.info(f"Trend request for: {keyword}")
    trend = get_trend_summary(keyword)
    return jsonify({
        'success': True,
        'trend': trend
    })


@app.route('/api/moodcheck', methods=['POST'])
@limiter.limit("10 per minute")
def moodcheck():
    """
    Main endpoint: Analyze images and return mood + products.

    Request body:
        - images: array of base64 encoded images (1-5)
        - prompt: optional string modifier (max 200 chars)

    Response:
        - success: boolean
        - vibe: mood profile object
        - products: array of product objects
        - search_queries_used: array of queries used
    """
    start_time = time.time()

    # Get request data
    data = request.get_json()

    # Log request
    image_count = len(data.get('images', [])) if data else 0
    prompt_preview = data.get('prompt', '')[:50] if data else ''
    logger.info(f"Moodcheck request: {image_count} images, prompt: '{prompt_preview}...'")

    # Step 1: Validate request
    is_valid, errors = validate_moodcheck_request(data)
    if not is_valid:
        logger.warning(f"Validation failed: {errors}")
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'details': errors
        }), 400

    images = data.get('images', [])
    prompt = data.get('prompt', '')
    max_products = min(data.get('max_products', 20), 50)  # Cap at 50

    # Step 2: Extract mood from images
    try:
        logger.info("Calling Vision API...")
        vision_start = time.time()
        mood_profile = extract_mood(images, prompt)
        vision_time = time.time() - vision_start
        logger.info(f"Vision API completed in {vision_time:.2f}s - Mood: {mood_profile.get('name')}")
    except Exception as e:
        logger.error(f"Vision API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to analyze images. Please try again.'
        }), 500

    # Step 3 & 4: Search for products AND fetch trend data in parallel
    search_queries = mood_profile.get('search_queries', [])
    budget = detect_budget_from_prompt(prompt)
    item_type = detect_item_type_from_prompt(prompt)
    vibe_name = mood_profile.get('name', '')

    # If specific item type detected, modify queries to focus on it
    if item_type:
        logger.info(f"Detected item type: {item_type} - modifying search queries")
        # Extract the specific item word from prompt (e.g., "boots" from "boho boots")
        item_word = None
        prompt_lower = prompt.lower()
        from services.shopping import ITEM_TYPE_KEYWORDS
        for keyword in ITEM_TYPE_KEYWORDS.get(item_type, []):
            if keyword in prompt_lower:
                item_word = keyword
                break

        # Create item-specific queries using the vibe name
        if item_word and vibe_name:
            search_queries = [
                f"{vibe_name} {item_word} women",
                f"{item_word} {vibe_name} style",
                f"womens {item_word} {mood_profile.get('mood', '')}",
                f"{item_word} {' '.join(mood_profile.get('textures', [])[:2])}",
                f"trendy {item_word} {vibe_name}",
                f"{item_word} outfit {vibe_name}",
            ]
            logger.info(f"Modified queries: {search_queries}")

    products = []
    trend = None

    def fetch_products():
        try:
            logger.info("Searching Google Shopping...")
            start = time.time()
            result = search_all_queries(
                search_queries,
                max_products=max_products,
                budget=budget,
                vibe_profile=mood_profile
            )
            logger.info(f"Shopping completed in {time.time() - start:.2f}s - Found {len(result)} products")
            return result
        except Exception as e:
            logger.error(f"Shopping API error: {e}")
            return []

    def fetch_trend():
        if not vibe_name:
            return None
        try:
            logger.info(f"Fetching trend data for '{vibe_name}'...")
            start = time.time()
            # Pass style_archetype for smarter keyword extraction
            style_archetype = mood_profile.get('style_archetype') if mood_profile else None
            result = get_trend_summary(vibe_name, style_archetype=style_archetype)
            logger.info(f"Trend data fetched in {time.time() - start:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Trend API error: {e}")
            return None

    # Run both in parallel
    parallel_start = time.time()
    with ThreadPoolExecutor(max_workers=2) as executor:
        products_future = executor.submit(fetch_products)
        trend_future = executor.submit(fetch_trend)
        products = products_future.result()
        trend = trend_future.result()
    logger.info(f"Parallel fetch completed in {time.time() - parallel_start:.2f}s")

    # Filter by item type if detected
    if item_type:
        products = filter_by_item_type(products, item_type)
        logger.info(f"Filtered to {len(products)} {item_type} items")

    # Step 5: Build response
    response = {
        'success': True,
        'vibe': {
            'name': mood_profile.get('name', 'Your Mood'),
            'mood': mood_profile.get('mood', ''),
            'color_palette': mood_profile.get('color_palette', []),
            'textures': mood_profile.get('textures', []),
            'key_pieces': mood_profile.get('key_pieces', []),
            'avoid': mood_profile.get('avoid', [])
        },
        'trend': trend,
        'products': products,
        'search_queries_used': search_queries[:8],
        'detected_item_type': item_type  # Frontend can use this to pre-select filter
    }

    total_time = time.time() - start_time
    logger.info(f"Moodcheck completed in {total_time:.2f}s")

    return jsonify(response), 200


# Aesthetic-specific signature accessories
AESTHETIC_ACCESSORIES = {
    "western": ["cowboy boots women", "western belt women", "turquoise jewelry", "fringe bag", "cowgirl hat"],
    "coastal": ["swimsuit women", "bikini set", "beach cover up", "straw tote bag", "espadrilles women"],
    "tropical": ["swimsuit women", "bikini set", "sarong wrap", "raffia bag", "platform sandals"],
    "beach": ["swimsuit women", "bikini set", "beach dress", "woven tote", "slide sandals"],
    "boho": ["fringe boots women", "layered necklaces", "wide brim hat", "embroidered bag", "ankle boots suede"],
    "bohemian": ["fringe boots women", "statement earrings", "floppy hat", "crossbody bag leather", "gladiator sandals"],
    "minimalist": ["structured tote bag", "simple gold jewelry", "white sneakers women", "leather belt slim", "watch women minimal"],
    "quiet luxury": ["cashmere scarf", "leather loafers women", "gold hoops small", "structured handbag", "ballet flats leather"],
    "parisian": ["ballet flats women", "silk scarf", "structured handbag", "gold jewelry classic", "kitten heels"],
    "athleisure": ["running sneakers women", "gym bag", "sports bra", "leggings high waist", "baseball cap"],
    "glamorous": ["statement earrings", "clutch bag evening", "strappy heels", "sparkle jewelry", "evening bag"],
    "mob wife": ["fur coat women", "gold chunky jewelry", "designer sunglasses", "leopard print heels", "statement handbag"],
    "cottagecore": ["mary jane shoes", "wicker basket bag", "pearl jewelry", "floral headband", "lace socks"],
    "scandinavian": ["minimalist watch", "leather backpack", "wool scarf", "white sneakers clean", "structured bag"],
    "corporate": ["structured tote leather", "pointed toe heels", "pearl earrings", "silk blouse", "watch classic women"],
    "old money": ["loafers leather women", "pearl necklace", "silk scarf", "tennis bracelet", "ballet flats"],
    "coquette": ["ballet flats bow", "ribbon hair accessories", "pearl jewelry", "mini bag", "mary janes"],
    "dark academia": ["oxford shoes women", "leather satchel", "vintage watch", "gold rimmed glasses", "wool beret"],
    "grunge": ["combat boots women", "choker necklace", "crossbody bag chain", "silver rings", "platform boots"],
    "vintage": ["cat eye sunglasses", "pearl earrings", "structured handbag", "heels kitten", "silk scarf vintage"],
    "streetwear": ["chunky sneakers", "bucket hat", "crossbody bag", "baseball cap", "platform sneakers"],
}


@app.route('/api/more-products', methods=['POST'])
@limiter.limit("20 per minute")
def more_products():
    """
    Fetch more products for an existing vibe profile.
    Uses different search query variations to get fresh results.

    Request body:
        - vibe_profile: the mood profile object from initial request
        - exclude_ids: array of product IDs to exclude (already shown)
        - max_products: number of products to return (default 20)

    Response:
        - success: boolean
        - products: array of new product objects
    """
    start_time = time.time()

    data = request.get_json()
    if not data or 'vibe_profile' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing vibe_profile'
        }), 400

    vibe_profile = data['vibe_profile']
    exclude_ids = set(data.get('exclude_ids', []))
    max_products = min(data.get('max_products', 20), 30)

    logger.info(f"More products request for '{vibe_profile.get('name', 'Unknown')}', excluding {len(exclude_ids)} items")

    # Generate alternative search queries to get fresh results
    vibe_name = vibe_profile.get('name', '')
    key_pieces = vibe_profile.get('key_pieces', [])
    textures = vibe_profile.get('textures', [])
    color_palette = vibe_profile.get('color_palette', [])

    # Create varied queries using different combinations
    alt_queries = []

    # Add aesthetic-specific accessories first (signature items for the vibe)
    vibe_lower = vibe_name.lower()
    for aesthetic_key, accessories in AESTHETIC_ACCESSORIES.items():
        if aesthetic_key in vibe_lower:
            for accessory in accessories[:3]:  # Top 3 signature accessories
                alt_queries.append(f"{accessory} {vibe_name}")
            logger.info(f"Added {aesthetic_key} accessories: {accessories[:3]}")
            break

    # Use key pieces with vibe name
    for piece in key_pieces[:4]:
        alt_queries.append(f"{piece} {vibe_name} style women")

    # Use textures
    for texture in textures[:2]:
        alt_queries.append(f"{texture} {vibe_name} clothing women")

    # Use colors
    for color in color_palette[:2]:
        color_name = color.get('name', '') if isinstance(color, dict) else color
        if color_name:
            alt_queries.append(f"{color_name} {vibe_name} fashion women")

    # Add some general style queries
    alt_queries.extend([
        f"{vibe_name} outfit ideas women",
        f"{vibe_name} wardrobe essentials",
        f"trending {vibe_name} fashion"
    ])

    logger.info(f"Alternative queries: {alt_queries[:6]}")

    try:
        # Search with alternative queries
        products = search_all_queries(
            alt_queries[:8],
            max_products=max_products + len(exclude_ids),  # Get extra to account for exclusions
            budget=None,
            vibe_profile=vibe_profile
        )

        # Filter out already-shown products
        fresh_products = []
        for p in products:
            product_id = p.get('id', '') + p.get('product_url', '')
            if product_id not in exclude_ids:
                fresh_products.append(p)
                if len(fresh_products) >= max_products:
                    break

        logger.info(f"More products completed in {time.time() - start_time:.2f}s - Found {len(fresh_products)} new products")

        return jsonify({
            'success': True,
            'products': fresh_products
        }), 200

    except Exception as e:
        logger.error(f"More products error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch more products'
        }), 500


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


if __name__ == '__main__':
    logger.info(f"Starting Moodboard API on port {Config.PORT}")
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )
