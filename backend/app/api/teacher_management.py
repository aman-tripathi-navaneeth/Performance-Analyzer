from flask import Blueprint, request, jsonify
from app.models.user_models import UserManager
from app.api.auth import token_required, admin_required

def require_admin(f):
    """Combined decorator for token and admin requirements"""
    return token_required(admin_required(f))
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

teacher_mgmt_bp = Blueprint('teacher_management', __name__)

@teacher_mgmt_bp.route('/teachers', methods=['GET'])
@require_admin
def get_all_teachers():
    """
    Get all teachers
    GET /api/v1/admin/teachers
    Requires admin authentication
    """
    try:
        logger.info("Admin requesting all teachers list")
        
        user_manager = UserManager()
        teachers = user_manager.get_all_teachers()
        
        logger.info(f"Retrieved {len(teachers)} teachers")
        
        return jsonify({
            'success': True,
            'data': {
                'teachers': teachers,
                'total_count': len(teachers)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving teachers: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error retrieving teachers: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/teachers', methods=['POST'])
@require_admin
def add_teacher():
    """
    Add a new teacher
    POST /api/v1/admin/teachers
    Requires admin authentication
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field.title()} is required'
                }), 400
        
        email = data['email'].strip().lower()
        password = data['password'].strip()
        name = data['name'].strip()
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400
        
        # Validate name
        if len(name) < 2:
            return jsonify({
                'success': False,
                'error': 'Name must be at least 2 characters long'
            }), 400
        
        logger.info(f"Admin adding new teacher: {email}")
        
        user_manager = UserManager()
        result = user_manager.add_teacher(email, password, name)
        
        if result['success']:
            logger.info(f"Successfully added teacher: {email}")
            return jsonify({
                'success': True,
                'message': 'Teacher added successfully',
                'data': result['teacher']
            }), 201
        else:
            logger.warning(f"Failed to add teacher: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Error adding teacher: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error adding teacher: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
@require_admin
def update_teacher(teacher_id):
    """
    Update teacher information
    PUT /api/v1/admin/teachers/{teacher_id}
    Requires admin authentication
    """
    try:
        data = request.get_json()
        
        # For now, we'll implement basic update functionality
        # This can be extended based on requirements
        
        logger.info(f"Admin updating teacher ID: {teacher_id}")
        
        return jsonify({
            'success': True,
            'message': 'Teacher update functionality coming soon',
            'data': {'teacher_id': teacher_id}
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating teacher: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error updating teacher: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/teachers/<int:teacher_id>/toggle-status', methods=['POST'])
@require_admin
def toggle_teacher_status(teacher_id):
    """
    Toggle teacher active/inactive status
    POST /api/v1/admin/teachers/{teacher_id}/toggle-status
    Requires admin authentication
    """
    try:
        logger.info(f"Admin toggling status for teacher ID: {teacher_id}")
        
        # This would implement the toggle functionality
        # For now, return a placeholder response
        
        return jsonify({
            'success': True,
            'message': 'Teacher status toggle functionality coming soon',
            'data': {'teacher_id': teacher_id}
        }), 200
        
    except Exception as e:
        logger.error(f"Error toggling teacher status: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error toggling teacher status: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/sections', methods=['GET'])
@require_admin
def get_all_sections():
    """
    Get all sections
    GET /api/v1/admin/sections
    Requires admin authentication
    """
    try:
        logger.info("Admin requesting all sections list")
        
        user_manager = UserManager()
        sections = user_manager.get_all_sections()
        
        logger.info(f"Retrieved {len(sections)} sections")
        
        return jsonify({
            'success': True,
            'data': {
                'sections': sections,
                'total_count': len(sections)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving sections: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error retrieving sections: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/sections', methods=['POST'])
@require_admin
def add_section():
    """
    Add a new section
    POST /api/v1/admin/sections
    Requires admin authentication
    """
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Section name is required'
            }), 400
        
        section_name = data['name'].strip().upper()
        
        # Validate section name
        if len(section_name) < 1:
            return jsonify({
                'success': False,
                'error': 'Section name cannot be empty'
            }), 400
        
        logger.info(f"Admin adding new section: {section_name}")
        
        user_manager = UserManager()
        result = user_manager.add_section(section_name)
        
        if result['success']:
            logger.info(f"Successfully added section: {section_name}")
            return jsonify({
                'success': True,
                'message': 'Section added successfully',
                'data': result['section']
            }), 201
        else:
            logger.warning(f"Failed to add section: {result['error']}")
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Error adding section: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error adding section: {str(e)}'
        }), 500

@teacher_mgmt_bp.route('/dashboard-stats', methods=['GET'])
@require_admin
def get_admin_dashboard_stats():
    """
    Get admin dashboard statistics
    GET /api/v1/admin/dashboard-stats
    Requires admin authentication
    """
    try:
        logger.info("Admin requesting dashboard statistics")
        
        user_manager = UserManager()
        
        # Get basic stats
        teachers = user_manager.get_all_teachers()
        sections = user_manager.get_all_sections()
        
        # Count active vs inactive teachers
        active_teachers = len([t for t in teachers if t['is_active']])
        inactive_teachers = len([t for t in teachers if not t['is_active']])
        
        # Get recent teachers (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_teachers = [
            t for t in teachers 
            if t['created_at'] and datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')) > thirty_days_ago
        ]
        
        stats = {
            'total_teachers': len(teachers),
            'active_teachers': active_teachers,
            'inactive_teachers': inactive_teachers,
            'total_sections': len(sections),
            'recent_teachers_count': len(recent_teachers),
            'recent_teachers': recent_teachers[:5]  # Last 5 recent teachers
        }
        
        logger.info(f"Retrieved admin dashboard stats: {stats['total_teachers']} teachers, {stats['total_sections']} sections")
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving admin dashboard stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error retrieving dashboard stats: {str(e)}'
        }), 500