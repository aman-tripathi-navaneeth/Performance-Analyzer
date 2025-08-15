#!/usr/bin/env python3
"""
Analyze SIS login form structure
"""

import requests
from bs4 import BeautifulSoup

def analyze_form():
    """Analyze the login form"""
    try:
        response = requests.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("🔍 SIS Login Form Analysis")
        print("=" * 40)
        
        # Find forms
        forms = soup.find_all('form')
        print(f"📋 Found {len(forms)} form(s)")
        
        for i, form in enumerate(forms):
            print(f"\n📝 Form {i+1}:")
            print(f"   Action: {form.get('action', 'Not specified')}")
            print(f"   Method: {form.get('method', 'GET')}")
            
            # Find inputs
            inputs = form.find_all('input')
            print(f"   Inputs ({len(inputs)}):")
            
            for inp in inputs:
                name = inp.get('name', 'No name')
                input_type = inp.get('type', 'text')
                placeholder = inp.get('placeholder', '')
                print(f"     - {name}: {input_type} (placeholder: '{placeholder}')")
        
        # Look for specific elements
        print(f"\n🔍 Specific Elements:")
        
        # Check for common login field patterns
        username_field = (soup.find('input', {'name': 'username'}) or 
                         soup.find('input', {'name': 'user'}) or
                         soup.find('input', {'name': 'login'}) or
                         soup.find('input', {'name': 'roll'}) or
                         soup.find('input', {'name': 'student_id'}))
        
        password_field = (soup.find('input', {'name': 'password'}) or
                         soup.find('input', {'name': 'pass'}) or
                         soup.find('input', {'name': 'pwd'}))
        
        if username_field:
            print(f"   ✅ Username field: {username_field.get('name')} (type: {username_field.get('type')})")
        else:
            print("   ❌ No username field found")
        
        if password_field:
            print(f"   ✅ Password field: {password_field.get('name')} (type: {password_field.get('type')})")
        else:
            print("   ❌ No password field found")
        
        # Show relevant HTML snippet
        print(f"\n📄 Form HTML:")
        print("-" * 40)
        for form in forms:
            print(form.prettify())
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    analyze_form()