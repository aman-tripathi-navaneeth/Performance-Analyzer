import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/performance_analyzer')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Supported file extensions
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Subject types
    SUBJECT_TYPES = {
        'REGULAR': 'regular',  # Mid-term, unit tests
        'CRT': 'crt',         # Weekly CRT scores
        'PROGRAMMING': 'programming'  # Competitive programming
    }