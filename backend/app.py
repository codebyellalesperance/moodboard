from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from utils.validation import validate_moodcheck_request

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
    """
    # Get request data
    data = request.get_json()

    # Validate request
    is_valid, errors = validate_moodcheck_request(data)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': 'Invalid request',
            'details': errors
        }), 400

    # TODO: Implement mood extraction and product search
    return jsonify({
        'success': False,
        'error': 'Not fully implemented yet',
        'message': 'Validation passed! Images and prompt received.'
    }), 501

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )
