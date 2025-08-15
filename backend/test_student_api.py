#!/usr/bin/env python3
"""
Test the enhanced student API to see academic insights
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.performance_models import Student
import json

def test_student_api():
    """Test the student API with a real student"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING ENHANCED STUDENT API ===")
        
        # Get a student from the new data we uploaded
        student = Student.query.filter_by(student_roll_number='22A91A0509').first()  # Dhruv Agarwal with 74%
        
        if not student:
            print("❌ Student 22A91A0501 not found")
            return
        
        print(f"✅ Found student: {student.first_name} {student.last_name} ({student.student_roll_number})")
        
        # Test the API endpoint
        with app.test_client() as client:
            # Test student detail endpoint
            response = client.get(f'/api/v1/students/{student.student_roll_number}')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ API Response successful")
                print(f"📊 Student Detail Data:")
                print(json.dumps(data['data'], indent=2))
            else:
                print(f"❌ API Error: {response.status_code}")
                print(response.get_json())
            
            print("\n" + "="*50)
            
            # Test performance endpoint (try both UUID and roll number)
            print(f"Testing performance endpoint with UUID: {student.id}")
            response = client.get(f'/api/v1/students/{student.id}/performance')
            
            if response.status_code != 200:
                print(f"UUID failed, trying with roll number: {student.student_roll_number}")
                # The performance endpoint expects UUID, let's check the route definition
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Performance API Response successful")
                
                # Extract and display insights
                insights = data['data'].get('insights', {})
                print(f"\n🎓 ACADEMIC INSIGHTS FOR {student.first_name} {student.last_name}:")
                print(f"📈 Performance Level: {insights.get('performance_level', 'N/A')}")
                print(f"📋 Academic Status: {insights.get('academic_status', 'N/A')}")
                print(f"🎯 Overall Grade: {insights.get('overall_grade', 'N/A')}")
                print(f"📊 Consistency: {insights.get('consistency', 'N/A')} ({insights.get('consistency_score', 0)}%)")
                
                print(f"\n💪 STRENGTHS:")
                for strength in insights.get('strengths', []):
                    print(f"  ✅ {strength}")
                
                print(f"\n⚠️  AREAS FOR IMPROVEMENT:")
                for weakness in insights.get('areas_for_improvement', []):
                    print(f"  🔸 {weakness}")
                
                print(f"\n📝 RECOMMENDATIONS:")
                for rec in insights.get('recommendations', []):
                    print(f"  💡 {rec}")
                
                print(f"\n📖 ACADEMIC SUMMARY:")
                print(f"  {insights.get('academic_summary', 'No summary available')}")
                
                # Show subject performance
                subjects = data['data'].get('subjects_performance', {})
                print(f"\n📚 SUBJECT PERFORMANCE:")
                for subject_name, subject_data in subjects.items():
                    stats = subject_data['statistics']
                    print(f"  📖 {subject_name}: {stats['average_percentage']}% (Grade: {stats['grade']}) - {stats['improvement_trend'].title()}")
                
            else:
                print(f"❌ Performance API Error: {response.status_code}")
                print(response.get_json())

if __name__ == "__main__":
    test_student_api()