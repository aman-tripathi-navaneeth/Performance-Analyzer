from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Configure CORS for React frontend - Enhanced configuration
    CORS(app, 
         origins=[
             "http://localhost:3000",  # React development server
             "http://localhost:3001",  # Alternative React port
             "http://localhost:3002",  # Alternative React port
             "http://localhost:5173",  # Vite development server
             "http://127.0.0.1:3000",  # Alternative localhost
             "http://127.0.0.1:3001",  # Alternative localhost
             "http://127.0.0.1:3002",  # Alternative localhost
             "http://127.0.0.1:5173",  # Alternative localhost for Vite
             # Add production frontend URL when deployed
             # "https://your-frontend-domain.com"
         ],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
         allow_headers=[
             "Content-Type", 
             "Authorization", 
             "X-Requested-With",
             "Accept",
             "Origin",
             "Access-Control-Request-Method",
             "Access-Control-Request-Headers",
             "Cache-Control",
             "Pragma"
         ],
         expose_headers=[
             "Content-Range",
             "X-Content-Range",
             "Access-Control-Allow-Origin"
         ],
         supports_credentials=True,
         max_age=86400  # Cache preflight requests for 24 hours
    )
    
    # Initialize database
    db.init_app(app)
    
    # Ensure upload directory exists
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder
    
    # Register API blueprints
    from app.api.uploads import uploads_bp
    from app.api.students import students_bp
    from app.api.analytics import analytics_bp
    from app.api.auth import auth_bp
    
    # Add manual CORS headers for additional safety
    @app.after_request
    def after_request(response):
        # Get the origin from the request
        origin = request.headers.get('Origin')
        
        # List of allowed origins
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:3002",
            "http://localhost:5173", 
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:3002",
            "http://127.0.0.1:5173"
        ]
        
        # Set CORS headers if origin is allowed
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Cache-Control, Pragma'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '86400'
        
        return response
    
    # Handle preflight OPTIONS requests
    @app.before_request
    def handle_preflight():
        from flask import request
        if request.method == "OPTIONS":
            response = make_response()
            origin = request.headers.get('Origin')
            
            allowed_origins = [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://localhost:3002",
                "http://localhost:5173", 
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "http://127.0.0.1:3002",
                "http://127.0.0.1:5173"
            ]
            
            if origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH'
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers, Cache-Control, Pragma'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = '86400'
            
            return response
    
    # Register blueprints with API v1 prefix
    app.register_blueprint(uploads_bp, url_prefix='/api/v1/upload')
    app.register_blueprint(students_bp, url_prefix='/api/v1/students')
    app.register_blueprint(analytics_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    
    # Register CORS test blueprint
    from app.api.cors_test import cors_test_bp
    app.register_blueprint(cors_test_bp, url_prefix='/api/v1/cors')
    
    # Register teacher management blueprint
    from app.api.teacher_management import teacher_mgmt_bp
    app.register_blueprint(teacher_mgmt_bp, url_prefix='/api/v1/admin')
    
    # Register SIS checker blueprint
    from app.api.sis_checker import sis_checker_bp
    app.register_blueprint(sis_checker_bp, url_prefix='/api/v1/sis')
    
    return app