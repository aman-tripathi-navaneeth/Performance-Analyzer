#!/usr/bin/env python3
"""
Comprehensive debugging script for class performance API
"""
import urllib.request
import json
import sqlite3
import sys
import os

def test_database_direct():
    """Test database directly"""
    print("=" * 60)
    print("🔍 TESTING DATABASE DIRECTLY")
    print("=" * 60)
    
    try:
        # Connect to database
        db_path = "instance/performance_analyzer.db"
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Available tables: {[table[0] for table in tables]}")
        
        # Check subjects table
        cursor.execute("SELECT * FROM subjects LIMIT 5;")
        subjects = cursor.fetchall()
        print(f"📚 Sample subjects: {subjects}")
        
        # Check students table
        cursor.execute("SELECT * FROM students LIMIT 5;")
        students = cursor.fetchall()
        print(f"👥 Sample students: {students}")
        
        # Check performance records
        cursor.execute("SELECT * FROM performance_records LIMIT 5;")
        records = cursor.fetchall()
        print(f"📝 Sample performance records: {records}")
        
        # Check assessments
        cursor.execute("SELECT * FROM assessments LIMIT 5;")
        assessments = cursor.fetchall()
        print(f"📋 Sample assessments: {assessments}")
        
        # Check specific year/section combinations
        cursor.execute("""
            SELECT DISTINCT year, section, COUNT(*) as count 
            FROM subjects 
            GROUP BY year, section 
            ORDER BY year, section;
        """)
        year_sections = cursor.fetchall()
        print(f"🎯 Available year/section combinations:")
        for ys in year_sections:
            print(f"   Year {ys[0]}, Section {ys[1]}: {ys[2]} subjects")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

def test_api_endpoints():
    """Test various API endpoints"""
    print("\n" + "=" * 60)
    print("🔍 TESTING API ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://localhost:5000/api/v1"
    
    # Test endpoints to try
    endpoints = [
        "/class/performance/1/CSEA",
        "/class/performance/2/CSE A",
        "/class/performance/2/CSEA", 
        "/class/performance/1/CSM",
        "/analytics/test-simple"
    ]
    
    for endpoint in endpoints:
        print(f"\n🌐 Testing: {base_url}{endpoint}")
        try:
            # URL encode the endpoint properly
            if "CSE A" in endpoint:
                endpoint = endpoint.replace("CSE A", "CSE%20A")
            
            url = f"{base_url}{endpoint}"
            print(f"   Full URL: {url}")
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                print(f"   ✅ Status: {response.status}")
                print(f"   📊 Success: {data.get('success', 'N/A')}")
                
                if 'data' in data:
                    if 'overall_stats' in data['data']:
                        stats = data['data']['overall_stats']
                        print(f"   👥 Students: {stats.get('total_students', 0)}")
                        print(f"   📚 Subjects: {stats.get('total_subjects', 0)}")
                        print(f"   📊 Average: {stats.get('overall_average', 0)}%")
                    else:
                        print(f"   📋 Data keys: {list(data['data'].keys())}")
                else:
                    print(f"   📋 Response keys: {list(data.keys())}")
                    
        except urllib.error.HTTPError as e:
            print(f"   ❌ HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_specific_class_query():
    """Test the specific SQL query that the API uses"""
    print("\n" + "=" * 60)
    print("🔍 TESTING SPECIFIC SQL QUERIES")
    print("=" * 60)
    
    try:
        db_path = "instance/performance_analyzer.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test the exact query from the API for year=2, section='CSE A'
        year = 2
        section = 'CSE A'
        
        print(f"🎯 Testing query for Year {year}, Section '{section}'")
        
        # Query 1: Get subjects for this year/section
        query1 = """
        SELECT 
            s.id,
            s.subject_name,
            s.base_subject_name,
            AVG(pr.marks_obtained * 100.0 / a.max_marks) as class_average,
            COUNT(DISTINCT pr.student_id) as student_count,
            COUNT(pr.id) as assessment_count
        FROM subjects s
        JOIN assessments a ON s.id = a.subject_id
        JOIN performance_records pr ON a.id = pr.assessment_id
        WHERE s.year = ? AND s.section = ?
        GROUP BY s.id, s.subject_name, s.base_subject_name
        """
        
        cursor.execute(query1, (year, section))
        subjects = cursor.fetchall()
        print(f"📚 Found {len(subjects)} subjects:")
        for subject in subjects:
            print(f"   - {subject[2]} ({subject[1]}): {subject[3]:.2f}% avg, {subject[4]} students")
        
        # Query 2: Get overall stats
        query2 = """
        SELECT 
            AVG(pr.marks_obtained * 100.0 / a.max_marks) as overall_average,
            COUNT(DISTINCT pr.student_id) as total_students,
            COUNT(DISTINCT s.id) as total_subjects,
            COUNT(pr.id) as total_assessments
        FROM performance_records pr
        JOIN assessments a ON pr.assessment_id = a.id
        JOIN subjects s ON a.subject_id = s.id
        WHERE s.year = ? AND s.section = ?
        """
        
        cursor.execute(query2, (year, section))
        stats = cursor.fetchone()
        print(f"📊 Overall stats: {stats[1]} students, {stats[2]} subjects, {stats[0]:.2f}% average")
        
        # Query 3: Get students
        query3 = """
        SELECT 
            st.id,
            st.student_roll_number,
            st.first_name,
            st.last_name,
            AVG(pr.marks_obtained * 100.0 / a.max_marks) as student_average,
            COUNT(pr.id) as assessment_count
        FROM students st
        JOIN performance_records pr ON st.id = pr.student_id
        JOIN assessments a ON pr.assessment_id = a.id
        JOIN subjects s ON a.subject_id = s.id
        WHERE s.year = ? AND s.section = ?
        GROUP BY st.id, st.student_roll_number, st.first_name, st.last_name
        """
        
        cursor.execute(query3, (year, section))
        students = cursor.fetchall()
        print(f"👥 Found {len(students)} students:")
        for student in students:
            print(f"   - {student[2]} {student[3]} ({student[1]}): {student[4]:.2f}% avg")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ SQL Query error: {e}")

def test_url_encoding():
    """Test different URL encoding scenarios"""
    print("\n" + "=" * 60)
    print("🔍 TESTING URL ENCODING")
    print("=" * 60)
    
    base_url = "http://localhost:5000/api/v1/class/performance/2"
    
    # Different ways to encode "CSE A"
    encodings = [
        "CSE A",           # No encoding
        "CSE%20A",         # Standard encoding
        "CSE+A",           # Plus encoding
        "CSEA",            # No space
    ]
    
    for encoding in encodings:
        print(f"\n🔗 Testing section encoding: '{encoding}'")
        url = f"{base_url}/{encoding}"
        print(f"   Full URL: {url}")
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                print(f"   ✅ Status: {response.status}")
                print(f"   📊 Success: {data.get('success', False)}")
                if data.get('success') and 'data' in data:
                    students = data['data'].get('overall_stats', {}).get('total_students', 0)
                    print(f"   👥 Students found: {students}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 COMPREHENSIVE CLASS PERFORMANCE DEBUGGING")
    print("=" * 60)
    
    # Change to backend directory
    if os.path.basename(os.getcwd()) != 'backend':
        if os.path.exists('backend'):
            os.chdir('backend')
        else:
            print("❌ Please run this script from the project root or backend directory")
            sys.exit(1)
    
    test_database_direct()
    test_api_endpoints()
    test_specific_class_query()
    test_url_encoding()
    
    print("\n" + "=" * 60)
    print("🏁 DEBUGGING COMPLETE")
    print("=" * 60)