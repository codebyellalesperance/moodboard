from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from utils.validation import validate_moodcheck_request
from services.vision import extract_mood
from services.shopping import search_all_queries, detect_budget_from_prompt

# Validate config on startup
Config.validate()

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'moodboard-api'
    })


@app.route('/api/moodcheck', methods=['POST'])
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

    # Get request data
    data = request.get_json()

    # Step 1: Validate request
    is_valid, errors = validate_moodcheck_request(data)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'details': errors
        }), 400

    images = data.get('images', [])
    prompt = data.get('prompt', '')

    # Step 2: Extract mood from images
    try:
        mood_profile = extract_mood(images, prompt)
    except Exception as e:
        print(f"Vision API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Unable to analyze images. Please try again.'
        }), 500

    # Step 3: Search for products
    try:
        search_queries = mood_profile.get('search_queries', [])
        budget = detect_budget_from_prompt(prompt)
        products = search_all_queries(search_queries, max_products=20, budget=budget)
    except Exception as e:
        print(f"Shopping API error: {e}")
        # Return mood even if product search fails
        products = []

    # Step 4: Build response
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
        'products': products,
        'search_queries_used': search_queries[:8]
    }

    return jsonify(response), 200


@app.errorhandler(500)
def internal_error(error):
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
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )
