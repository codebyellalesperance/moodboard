from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from utils.validation import validate_moodcheck_request
from utils.logger import logger
from services.vision import extract_mood
from services.shopping import search_all_queries, detect_budget_from_prompt
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

    # Step 3: Search for products
    try:
        logger.info("Searching Google Shopping...")
        shopping_start = time.time()
        search_queries = mood_profile.get('search_queries', [])
        budget = detect_budget_from_prompt(prompt)
        products = search_all_queries(
            search_queries,
            max_products=max_products,
            budget=budget,
            vibe_profile=mood_profile
        )
        shopping_time = time.time() - shopping_start
        logger.info(f"Shopping completed in {shopping_time:.2f}s - Found {len(products)} products")
    except Exception as e:
        logger.error(f"Shopping API error: {e}")
        products = []

    # Step 4: Get trend data for the vibe
    trend = None
    vibe_name = mood_profile.get('name', '')
    if vibe_name:
        try:
            logger.info(f"Fetching trend data for '{vibe_name}'...")
            trend_start = time.time()
            trend = get_trend_summary(vibe_name)
            trend_time = time.time() - trend_start
            logger.info(f"Trend data fetched in {trend_time:.2f}s - Direction: {trend.get('direction')}")
        except Exception as e:
            logger.error(f"Trend API error: {e}")
            trend = None

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
        'search_queries_used': search_queries[:8]
    }

    total_time = time.time() - start_time
    logger.info(f"Moodcheck completed in {total_time:.2f}s")

    return jsonify(response), 200


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
