#!/usr/bin/env python3
"""
Test script for real SIS integration
This script will actually connect to the college SIS portal and attempt to login
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.sis_integration import SISIntegration
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_real_sis_connection():
    """Test connection to the real SIS portal"""
    print("🔗 Testing connection to SIS portal...")
    
    try:
        import requests
        response = requests.get('https://sis.idealtech.edu.in/student/index.php', timeout=10)
        
        if response.status_code == 200:
            print(f"✅ SIS portal is accessible (Status: {response.status_code})")
            print(f"📄 Page title: {response.text[:200]}...")
            return True
        else:
            print(f"❌ SIS portal returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot connect to SIS portal: {str(e)}")
        return False

def test_sis_login(roll_number, password=None):
    """Test SIS login with real credentials"""
    if not password:
        password = roll_number  # Use roll number as password
    
    print(f"\n🔐 Testing SIS login for roll number: {roll_number}")
    print(f"🔑 Using password: {password}")
    
    try:
        # Initialize real SIS integration (not mock)
        sis = SISIntegration()
        
        # Attempt login
        print("📝 Attempting to login to SIS portal...")
        login_success = sis.login_student(roll_number, password)
        
        if login_success:
            print("✅ Login successful!")
            
            # Try to fetch results
            print("📊 Fetching student results...")
            results = sis.get_student_results(roll_number)
            
            if results:
                print("✅ Results fetched successfully!")
                print(f"📈 Total subjects: {results.get('total_subjects', 0)}")
                print(f"📈 Passed subjects: {results.get('passed_subjects', 0)}")
                print(f"📈 Backlogs: {results.get('backlog_count', 0)}")
                
                if results.get('backlogs'):
                    print("\n📋 Backlog details:")
                    for i, backlog in enumerate(results['backlogs'], 1):
                        print(f"  {i}. {backlog.get('subject_name', 'Unknown')} - {backlog.get('grade', 'N/A')}")
                
                return results
            else:
                print("❌ Could not fetch results data")
                return None
        else:
            print("❌ Login failed - check credentials")
            return None
            
    except Exception as e:
        print(f"❌ Error during SIS integration: {str(e)}")
        return None

def test_full_backlog_check(roll_number, password=None):
    """Test the complete backlog checking process"""
    if not password:
        password = roll_number
    
    print(f"\n🎓 Full backlog check for: {roll_number}")
    print("=" * 50)
    
    try:
        # Use the main backlog checking method
        sis = SISIntegration()
        result = sis.check_student_backlogs(roll_number, password)
        
        print(f"✅ Check completed!")
        print(f"📊 Success: {result['success']}")
        
        if result['success']:
            print(f"🎯 Roll Number: {result['roll_number']}")
            print(f"📚 Total Subjects: {result['total_subjects']}")
            print(f"✅ Passed Subjects: {result['passed_subjects']}")
            print(f"❌ Backlogs: {result['backlog_count']}")
            print(f"📈 Overall Status: {result['overall_status']}")
            
            if result['backlogs']:
                print(f"\n📋 Backlog Details:")
                for i, backlog in enumerate(result['backlogs'], 1):
                    print(f"  {i}. {backlog.get('subject_name', 'Unknown Subject')}")
                    print(f"     Code: {backlog.get('subject_code', 'N/A')}")
                    print(f"     Semester: {backlog.get('semester', 'N/A')}")
                    print(f"     Marks: {backlog.get('marks', 'N/A')}")
                    print(f"     Grade: {backlog.get('grade', 'N/A')}")
                    print()
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None

def main():
    """Main test function"""
    print("🎓 Real SIS Integration Test")
    print("=" * 40)
    
    # Step 1: Test connection
    if not test_real_sis_connection():
        print("❌ Cannot proceed - SIS portal is not accessible")
        return
    
    # Step 2: Get test credentials
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
    
    # Step 3: Test the integration
    print("\n" + "=" * 40)
    result = test_full_backlog_check(roll_number, password)
    
    if result:
        print("\n🎉 Test completed successfully!")
        if result['success'] and result['backlog_count'] == 0:
            print("🎊 Great news - No backlogs found!")
        elif result['success'] and result['backlog_count'] > 0:
            print(f"⚠️  Found {result['backlog_count']} backlog(s)")
    else:
        print("\n❌ Test failed")
    
    print("\n" + "=" * 40)
    print("💡 Tips:")
    print("- Make sure you have the correct roll number")
    print("- Check if the password is correct (or try using roll number as password)")
    print("- Ensure the SIS portal is accessible from your network")
    print("- Check if there are any captcha or additional security measures")

if __name__ == "__main__":
    main()