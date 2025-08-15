"""
SIS Checker API - Backend endpoint for checking student backlogs
"""

from flask import Blueprint, request, jsonify
import logging
from app.services.sis_integration import SISIntegration, MockSISIntegration
import os

logger = logging.getLogger(__name__)

sis_checker_bp = Blueprint('sis_checker', __name__)

# Use mock implementation for development/testing
USE_MOCK_SIS = os.getenv('USE_MOCK_SIS', 'true').lower() == 'true'

@sis_checker_bp.route('/check-backlogs', methods=['POST'])
def check_student_backlogs():
    """
    Check student backlogs from SIS portal
    
    POST /api/v1/sis/check-backlogs
    Body: {
        "roll_number": "student_roll_number",
        "password": "optional_password"  // defaults to roll_number
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "roll_number": "...",
            "backlog_count": 0,
            "backlogs": [...],
            "total_subjects": 45,
            "passed_subjects": 45,
            "overall_status": "clear"
        }
    }
    """
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
        
        # Initialize SIS integration service
        if USE_MOCK_SIS:
            logger.info("Using mock SIS integration for testing")
            sis_service = MockSISIntegration()
        else:
            logger.info("Using real SIS integration")
            sis_service = SISIntegration()
        
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

@sis_checker_bp.route('/batch-check-backlogs', methods=['POST'])
def batch_check_backlogs():
    """
    Check backlogs for multiple students
    
    POST /api/v1/sis/batch-check-backlogs
    Body: {
        "roll_numbers": ["roll1", "roll2", "roll3"],
        "use_roll_as_password": true
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "total_checked": 3,
            "successful_checks": 2,
            "failed_checks": 1,
            "results": [...]
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        roll_numbers = data.get('roll_numbers', [])
        if not roll_numbers or not isinstance(roll_numbers, list):
            return jsonify({
                'success': False,
                'error': 'roll_numbers array is required'
            }), 400
        
        use_roll_as_password = data.get('use_roll_as_password', True)
        
        logger.info(f"Batch checking backlogs for {len(roll_numbers)} students")
        
        # Initialize SIS integration service
        if USE_MOCK_SIS:
            sis_service = MockSISIntegration()
        else:
            sis_service = SISIntegration()
        
        results = []
        successful_checks = 0
        failed_checks = 0
        
        for roll_number in roll_numbers:
            try:
                password = roll_number if use_roll_as_password else None
                result = sis_service.check_student_backlogs(roll_number, password)
                
                if result['success']:
                    successful_checks += 1
                else:
                    failed_checks += 1
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error checking backlogs for {roll_number}: {str(e)}")
                failed_checks += 1
                results.append({
                    'success': False,
                    'roll_number': roll_number,
                    'error': str(e),
                    'backlog_count': 0,
                    'backlogs': [],
                    'total_subjects': 0,
                    'passed_subjects': 0,
                    'overall_status': 'error'
                })
        
        return jsonify({
            'success': True,
            'data': {
                'total_checked': len(roll_numbers),
                'successful_checks': successful_checks,
                'failed_checks': failed_checks,
                'results': results
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch_check_backlogs: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@sis_checker_bp.route('/test-connection', methods=['GET'])
def test_sis_connection():
    """
    Test connection to SIS portal
    
    GET /api/v1/sis/test-connection
    
    Returns connection status and portal availability
    """
    try:
        if USE_MOCK_SIS:
            return jsonify({
                'success': True,
                'data': {
                    'status': 'connected',
                    'portal_url': 'https://sis.idealtech.edu.in/student/index.php',
                    'mode': 'mock',
                    'message': 'Using mock SIS integration for testing'
                }
            }), 200
        
        # Test real connection
        import requests
        
        try:
            response = requests.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
            if response.status_code == 200:
                return jsonify({
                    'success': True,
                    'data': {
                        'status': 'connected',
                        'portal_url': 'https://sis.idealtech.edu.in/student/index.php',
                        'mode': 'real',
                        'response_code': response.status_code,
                        'message': 'SIS portal is accessible'
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': f'SIS portal returned status code: {response.status_code}'
                }), 400
                
        except requests.exceptions.RequestException as e:
            return jsonify({
                'success': False,
                'error': f'Cannot connect to SIS portal: {str(e)}'
            }), 400
            
    except Exception as e:
        logger.error(f"Error testing SIS connection: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500