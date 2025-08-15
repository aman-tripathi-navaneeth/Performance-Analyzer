#!/usr/bin/env python3
"""
Test SIS login functionality with real credentials
"""

import requests
from bs4 import BeautifulSoup
import sys

def analyze_login_form():
    """Analyze the login form structure"""
    print("🔍 Analyzing SIS login form...")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        response = session.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all forms
        forms = soup.find_all('form')
        print(f"📋 Found {len(forms)} form(s)")
        
        for i, form in enumerate(forms):
            print(f"\n📝 Form {i+1}:")
            print(f"   Action: {form.get('action', 'Not specified')}")
            print(f"   Method: {form.get('method', 'GET')}")
            
            # Find all input fields
            inputs = form.find_all('input')
            print(f"   Input fields ({len(inputs)}):")
            
            for inp in inputs:
                input_type = inp.get('type', 'text')
                input_name = inp.get('name', 'No name')
                input_value = inp.get('value', '')
                input_placeholder = inp.get('placeholder', '')
                
                print(f"     - {input_name}: type='{input_type}', placeholder='{input_placeholder}', value='{input_value}'")
        
        # Look for specific login-related elements
        print(f"\n🔍 Looking for login elements...")
        
        # Common login field names
        login_fields = ['username', 'user', 'login', 'email', 'roll', 'student_id', 'userid']
        password_fields = ['password', 'pass', 'pwd']
        
        found_login = False
        found_password = False
        
        for field in login_fields:
            element = soup.find('input', {'name': field}) or soup.find('input', {'id': field})
            if element:
                print(f"   ✅ Found login field: {field}")
                found_login = True
        
        for field in password_fields:
            element = soup.find('input', {'name': field}) or soup.find('input', {'id': field})
            if element:
                print(f"   ✅ Found password field: {field}")
                found_password = True
        
        if found_login and found_password:
            print("✅ Login form structure looks good!")
        else:
            print("⚠️  Could not identify standard login fields")
        
        # Show the full HTML for manual inspection
        print(f"\n📄 Full HTML content:")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        
        return session, soup
        
    except Exception as e:
        print(f"❌ Error analyzing form: {str(e)}")
        return None, None

def test_login_attempt(roll_number, password):
    """Test actual login attempt"""
    print(f"\n🔐 Testing login for: {roll_number}")
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Get login page first
        login_response = session.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
        soup = BeautifulSoup(login_response.content, 'html.parser')
        
        # Find the form
        form = soup.find('form')
        if not form:
            print("❌ No form found on login page")
            return False
        
        # Prepare login data - try different field name combinations
        login_data_options = [
            {'username': roll_number, 'password': password},
            {'user': roll_number, 'pass': password},
            {'login': roll_number, 'password': password},
            {'roll': roll_number, 'password': password},
            {'student_id': roll_number, 'password': password},
            {'userid': roll_number, 'pwd': password},
        ]
        
        # Add any hidden fields
        hidden_inputs = soup.find_all('input', type='hidden')
        base_data = {}
        for hidden in hidden_inputs:
            name = hidden.get('name')
            value = hidden.get('value', '')
            if name:
                base_data[name] = value
        
        # Try each login data combination
        for i, login_data in enumerate(login_data_options):
            print(f"🔄 Attempt {i+1}: {login_data}")
            
            # Combine with hidden fields
            full_data = {**base_data, **login_data}
            
            # Get form action
            form_action = form.get('action', '')
            if form_action:
                if form_action.startswith('/'):
                    submit_url = 'https://sis.idealtech.edu.in' + form_action
                elif form_action.startswith('http'):
                    submit_url = form_action
                else:
                    submit_url = 'https://sis.idealtech.edu.in/student/' + form_action
            else:
                submit_url = 'https://sis.idealtech.edu.in/student/index.php'
            
            print(f"📤 Submitting to: {submit_url}")
            
            # Submit login
            response = session.post(submit_url, data=full_data, timeout=10)
            
            print(f"📥 Response status: {response.status_code}")
            print(f"📥 Response URL: {response.url}")
            print(f"📥 Response length: {len(response.text)} characters")
            
            # Check response content
            response_text = response.text.lower()
            
            # Success indicators
            success_indicators = ['dashboard', 'welcome', 'student portal', 'logout', 'profile', 'results']
            failure_indicators = ['invalid', 'error', 'incorrect', 'failed', 'try again', 'login']
            
            success_found = any(indicator in response_text for indicator in success_indicators)
            failure_found = any(indicator in response_text for indicator in failure_indicators)
            
            if success_found and not failure_found:
                print("✅ Login appears successful!")
                print(f"📄 First 500 chars of response:")
                print(response.text[:500])
                return True
            elif failure_found:
                print("❌ Login failed - found failure indicators")
            else:
                print("❓ Login result unclear")
            
            print(f"📄 Response preview:")
            print(response.text[:200])
            print()
        
        print("❌ All login attempts failed")
        return False
        
    except Exception as e:
        print(f"❌ Error during login test: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🎓 SIS Login Test")
    print("=" * 40)
    
    # First analyze the form
    session, soup = analyze_login_form()
    
    if not session or not soup:
        print("❌ Cannot proceed - failed to analyze login form")
        return
    
    # Get test credentials
    print("\n" + "=" * 40)
    print("📝 Enter test credentials:")
    
    roll_number = input("Roll Number: ").strip()
    if not roll_number:
        print("❌ Roll number is required")
        return
    
    use_roll_as_password = input(f"Use '{roll_number}' as password? (y/n): ").strip().lower()
    
    if use_roll_as_password == 'y':
        password = roll_number
    else:
        password = input("Password: ").strip()
        if not password:
            password = roll_number
    
    # Test login
    print("\n" + "=" * 40)
    success = test_login_attempt(roll_number, password)
    
    if success:
        print("\n🎉 Login test successful!")
        print("💡 The SIS integration should work with these credentials")
    else:
        print("\n❌ Login test failed")
        print("💡 Check credentials or form structure")

if __name__ == "__main__":
    main()