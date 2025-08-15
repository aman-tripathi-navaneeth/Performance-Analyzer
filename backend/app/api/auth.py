from flask import Blueprint, request, jsonify
from functools import wraps
from app.models.user_models import UserManager

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            result = user_manager.verify_token(token)
            if not result['valid']:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            # Pass user info to the route
            request.current_user = result['user']
            
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user') or request.current_user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        if not all([email, password, role]):
            return jsonify({'error': 'Email, password, and role are required'}), 400
        
        if role not in ['admin', 'teacher']:
            return jsonify({'error': 'Invalid role'}), 400
        
        result = user_manager.authenticate_user(email, password, role)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': result['user'],
                'token': result['token']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 401
    
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """User logout endpoint"""
    try:
        token = request.headers.get('Authorization')
        if token.startswith('Bearer '):
            token = token[7:]
        
        result = user_manager.logout_user(token)
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token():
    """Verify token and return user info"""
    return jsonify({
        'success': True,
        'user': request.current_user
    }), 200

@auth_bp.route('/teachers', methods=['GET'])
@token_required
@admin_required
def get_teachers():
    """Get all teachers (admin only)"""
    try:
        teachers = user_manager.get_all_teachers()
        return jsonify({
            'success': True,
            'teachers': teachers
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get teachers: {str(e)}'}), 500

@auth_bp.route('/teachers', methods=['POST'])
@token_required
@admin_required
def add_teacher():
    """Add a new teacher (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password', 'teacher123')  # Default password
        name = data.get('name')
        
        if not all([email, name]):
            return jsonify({'error': 'Email and name are required'}), 400
        
        result = user_manager.add_teacher(email, password, name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Teacher added successfully',
                'teacher': result['teacher']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
    
    except Exception as e:
        return jsonify({'error': f'Failed to add teacher: {str(e)}'}), 500

@auth_bp.route('/sections', methods=['GET'])
@token_required
def get_sections():
    """Get all sections"""
    try:
        sections = user_manager.get_all_sections()
        return jsonify({
            'success': True,
            'sections': sections
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get sections: {str(e)}'}), 500

@auth_bp.route('/sections', methods=['POST'])
@token_required
@admin_required
def add_section():
    """Add a new section (admin only)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        
        if not name:
            return jsonify({'error': 'Section name is required'}), 400
        
        result = user_manager.add_section(name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Section added successfully',
                'section': result['section']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
    
    except Exception as e:
        return jsonify({'error': f'Failed to add section: {str(e)}'}), 500