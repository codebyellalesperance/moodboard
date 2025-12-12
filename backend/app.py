from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Validate config on startup
Config.validate()

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'moodboard-api'
    })

@app.route('/api/moodcheck', methods=['POST'])
def moodcheck():
    """Main endpoint - to be implemented in later steps."""
    return jsonify({
        'success': False,
        'error': 'Not implemented yet'
    }), 501

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_ENV == 'development'
    )
