#!/usr/bin/env python3
"""
Simple Flask server for SIS integration testing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.sis_integration import MockSISIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
])

@app.route('/api/v1/sis/check-backlogs', methods=['POST'])
def check_student_backlogs():
    """Check student backlogs from SIS portal"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        roll_number = data.get('roll_number', '').strip()
        if not roll_number:
            return jsonify({
                'success': False,
                'error': 'Roll number is required'
            }), 400
        
        password = data.get('password', roll_number).strip()
        
        logger.info(f"Checking backlogs for student: {roll_number}")
        
        # Initialize SIS integration service (using mock for now)
        sis_service = MockSISIntegration()
        
        # Check backlogs
        result = sis_service.check_student_backlogs(roll_number, password)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to check backlogs'),
                'data': result
            }), 400
            
    except Exception as e:
        logger.error(f"Error in check_student_backlogs: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/v1/sis/test-connection', methods=['GET'])
def test_sis_connection():
    """Test connection to SIS portal"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'status': 'connected',
                'portal_url': 'https://sis.idealtech.edu.in/student/index.php',
                'mode': 'mock',
                'message': 'Using mock SIS integration for testing'
            }
        }), 200
    except Exception as e:
        logger.error(f"Error testing SIS connection: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SIS Integration Server',
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    print("🚀 Starting SIS Integration Server")
    print("=" * 50)
    print("📍 Server URL: http://localhost:5000")
    print("📍 API Base URL: http://localhost:5000/api/v1/sis")
    print("🧪 Health Check: http://localhost:5000/health")
    print("🔍 Test Endpoint: http://localhost:5000/api/v1/sis/test-connection")
    print("=" * 50)
    print("✅ CORS enabled for React frontend")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)