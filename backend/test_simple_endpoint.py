#!/usr/bin/env python3
"""
Test the simple endpoint
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_simple_endpoint():
    """Test the simple endpoint"""
    app = create_app()
    
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/api/v1/test-simple')
            print(f"Status: {response.status_code}")
            print(f"Data: {response.get_json()}")

if __name__ == "__main__":
    test_simple_endpoint()