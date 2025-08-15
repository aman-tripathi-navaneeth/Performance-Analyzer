from flask import Blueprint, jsonify, request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cors_test_bp = Blueprint('cors_test', __name__)

@cors_test_bp.route('/test', methods=['GET', 'POST', 'OPTIONS'])
def cors_test():
    """
    Simple CORS test endpoint
    GET /api/v1/cors/test
    """
    try:
        logger.info(f"CORS Test - Method: {request.method}")
        logger.info(f"CORS Test - Origin: {request.headers.get('Origin', 'No Origin')}")
        logger.info(f"CORS Test - Headers: {dict(request.headers)}")
        
        return jsonify({
            'success': True,
            'message': 'CORS test successful!',
            'method': request.method,
            'origin': request.headers.get('Origin', 'No Origin'),
            'user_agent': request.headers.get('User-Agent', 'No User Agent'),
            'timestamp': str(request.timestamp) if hasattr(request, 'timestamp') else 'N/A'
        }), 200
        
    except Exception as e:
        logger.error(f"CORS Test Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'CORS test failed: {str(e)}'
        }), 500

@cors_test_bp.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    GET /api/v1/cors/health
    """
    return jsonify({
        'success': True,
        'message': 'Backend server is running!',
        'status': 'healthy'
    }), 200