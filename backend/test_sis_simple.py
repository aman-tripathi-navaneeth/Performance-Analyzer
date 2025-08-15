#!/usr/bin/env python3
"""
Simple test to check SIS portal connectivity
"""

def test_sis_connection():
    """Test basic connection to SIS portal"""
    try:
        import requests
        print("🔗 Testing connection to SIS portal...")
        
        response = requests.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Content Length: {len(response.text)} characters")
        print(f"🌐 URL: {response.url}")
        
        # Check if it looks like a login page
        content_lower = response.text.lower()
        
        if 'login' in content_lower or 'username' in content_lower or 'password' in content_lower:
            print("✅ Looks like a login page - good!")
        else:
            print("⚠️  Doesn't look like a typical login page")
        
        # Show first 500 characters
        print("\n📄 First 500 characters of response:")
        print("-" * 50)
        print(response.text[:500])
        print("-" * 50)
        
        return True
        
    except ImportError:
        print("❌ 'requests' module not installed")
        print("💡 Run: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_sis_connection()