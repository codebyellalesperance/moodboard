"""
Moodboard Backend API
Flask server that processes images via GPT-4V and returns product recommendations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from services.vision import extract_mood
from services.shopping import search_products
from utils.validation import validate_moodcheck_request

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


@app.route('/api/moodcheck', methods=['POST'])
def moodcheck():
    """
    Main endpoint: analyze images and return mood + product recommendations.

    Request body:
        images: list of base64 data URIs (1-5 images)
        prompt: optional string (max 200 chars)

    Returns:
        success: bool
        vibe: mood profile object
        products: list of product objects
    """
    data = request.get_json()

    # Validate request
    validation_error = validate_moodcheck_request(data)
    if validation_error:
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'details': validation_error
        }), 400

    try:
        # Extract mood from images using GPT-4V
        images = data.get('images', [])
        prompt = data.get('prompt', '')

        mood_result = extract_mood(images, prompt)

        # Search for products based on mood
        products = search_products(mood_result)

        return jsonify({
            'success': True,
            'vibe': mood_result,
            'products': products,
            'search_queries_used': mood_result.get('search_queries', [])
        })

    except Exception as e:
        app.logger.error(f'Moodcheck error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to analyze images'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
