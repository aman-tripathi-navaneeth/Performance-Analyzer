#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from urllib.parse import quote, unquote

def test_url_encoding():
    """Test URL encoding for section names with spaces"""
    print("=== TESTING URL ENCODING FOR SECTIONS ===")
    
    app = create_app()
    
    sections_to_test = ["CSE A", "CSEA", "CSE B", "ECE"]
    
    with app.test_client() as client:
        for section in sections_to_test:
            print(f"\n🧪 Testing section: '{section}'")
            
            # Test with URL encoding
            encoded_section = quote(section)
            print(f"   Encoded: '{encoded_section}'")
            
            # Test the API call
            url = f'/api/v1/class/performance/2/{encoded_section}'
            print(f"   URL: {url}")
            
            response = client.get(url)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    class_data = data['data']
                    print(f"   ✅ Success: {class_data['class_name']}")
                    print(f"      Students: {class_data['overall_stats']['total_students']}")
                    print(f"      Average: {class_data['overall_stats']['overall_average']}%")
                else:
                    print(f"   ❌ API Error: {data.get('error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                error_text = response.get_data(as_text=True)
                print(f"      Response: {error_text[:200]}...")
            
            # Also test decoding
            decoded_section = unquote(encoded_section)
            print(f"   Decoded back: '{decoded_section}' (matches original: {decoded_section == section})")

if __name__ == "__main__":
    test_url_encoding()