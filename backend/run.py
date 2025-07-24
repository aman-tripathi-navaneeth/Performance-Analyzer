#!/usr/bin/env python3
"""
Development server entry point for Performance Analyzer Backend
This script is for local development only.
"""

from app import create_app
import os

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"🚀 Starting Performance Analyzer Backend...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"📊 Environment: Development")
    print(f"🔄 Auto-reload: Enabled")
    print("-" * 50)
    
    # Run the development server
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        use_reloader=True,
        threaded=True
    )