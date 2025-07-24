from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Configure CORS for React frontend
    CORS(app, 
         origins=[
             "http://localhost:3000",  # React development server
             "http://localhost:5173",  # Vite development server
             "http://127.0.0.1:3000",  # Alternative localhost
             "http://127.0.0.1:5173",  # Alternative localhost for Vite
             # Add production frontend URL when deployed
             # "https://your-frontend-domain.com"
         ],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
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
    
    # Register blueprints with API v1 prefix
    app.register_blueprint(uploads_bp, url_prefix='/api/v1/upload')
    app.register_blueprint(students_bp, url_prefix='/api/v1/students')
    app.register_blueprint(analytics_bp, url_prefix='/api/v1')
    
    return app