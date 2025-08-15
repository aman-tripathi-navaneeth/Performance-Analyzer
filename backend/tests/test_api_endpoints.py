import pytest
import json
import tempfile
import os
import pandas as pd
from io import BytesIO
from app import db
from app.models import Student, Subject, Assessment, PerformanceRecord
from datetime import date

class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    def create_sample_excel_file(self, data, filename="test_upload.xlsx"):
        """Helper method to create sample Excel files for testing"""
        df = pd.DataFrame(data)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        return excel_buffer
    
    def test_upload_endpoint_success(self, client, app):
        """Test successful file upload to /api/v1/upload/subject"""
        with app.app_context():
            # Create sample Excel data
            sample_data = {
                'Student ID': ['CS001', 'CS002', 'CS003'],
                'First Name': ['John', 'Jane', 'Bob'],
                'Last Name': ['Doe', 'Smith', 'Johnson'],
                'Marks': [85, 78, 92]
            }
            
            excel_file = self.create_sample_excel_file(sample_data)
            
            # Prepare form data
            form_data = {
                'file': (excel_file, 'test_upload.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                'subject_name': 'Mathematics',
                'assessment_name': 'Mid-term Exam',
                'assessment_date': '2024-01-15',
                'max_marks': '100'
            }
            
            # Make POST request
            response = client.post(
                '/api/v1/upload/subject',
                data=form_data,
                content_type='multipart/form-data'
            )
            
            # Assert response
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            assert response_data['success'] == True
            assert 'message' in response_data
            assert response_data['message'] == 'File processed successfully'
            
            # Check response data structure
            assert 'data' in response_data
            data = response_data['data']
            assert data['subject_name'] == 'Mathematics'
            assert data['assessment_name'] == 'Mid-term Exam'
            assert data['students_processed'] >= 0
            assert data['records_created'] >= 0
            assert data['total_rows'] == 3
            
            # Verify data was actually saved to database
            students = Student.query.all()
            assert len(students) >= 3
            
            subjects = Subject.query.all()
            assert len(subjects) >= 1
            assert subjects[0].subject_name == 'Mathematics'
            
            assessments = Assessment.query.all()
            assert len(assessments) >= 1
            assert assessments[0].assessment_name == 'Mid-term Exam'
            
            records = PerformanceRecord.query.all()
            assert len(records) >= 3
    
    def test_upload_endpoint_missing_file(self, client):
        """Test upload endpoint with missing file"""
        form_data = {
            'subject_name': 'Mathematics',
            'assessment_name': 'Mid-term Exam'
        }
        
        response = client.post(
            '/api/v1/upload/subject',
            data=form_data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] == False
        assert 'no file provided' in response_data['error'].lower()
    
    def test_upload_endpoint_missing_subject_name(self, client):
        """Test upload endpoint with missing subject name"""
        sample_data = {
            'Student ID': ['CS001'],
            'Name': ['John Doe'],
            'Marks': [85]
        }
        
        excel_file = self.create_sample_excel_file(sample_data)
        
        form_data = {
            'file': (excel_file, 'test.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            'assessment_name': 'Mid-term Exam'
        }
        
        response = client.post(
            '/api/v1/upload/subject',
            data=form_data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] == False
        assert 'subject name is required' in response_data['error'].lower()
    
    def test_upload_endpoint_invalid_file_type(self, client):
        """Test upload endpoint with invalid file type"""
        # Create a text file instead of Excel
        text_file = BytesIO(b"This is not an Excel file")
        
        form_data = {
            'file': (text_file, 'test.txt', 'text/plain'),
            'subject_name': 'Mathematics',
            'assessment_name': 'Mid-term Exam'
        }
        
        response = client.post(
            '/api/v1/upload/subject',
            data=form_data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['success'] == False
        assert 'invalid file type' in response_data['error'].lower()
    
    def test_student_performance_endpoint_success(self, client, app):
        """Test successful retrieval of student performance data"""
        with app.app_context():
            # Create test data
            subject = Subject(subject_name="Mathematics")
            db.session.add(subject)
            db.session.flush()
            
            student = Student(
                first_name="John",
                last_name="Doe",
                student_roll_number="CS001"
            )
            db.session.add(student)
            db.session.flush()
            
            # Create multiple assessments
            assessment1 = Assessment(
                assessment_name="Mid-term Exam",
                assessment_date=date(2024, 1, 15),
                max_marks=100,
                subject_id=subject.id
            )
            assessment2 = Assessment(
                assessment_name="Unit Test 1",
                assessment_date=date(2024, 2, 1),
                max_marks=50,
                subject_id=subject.id
            )
            db.session.add_all([assessment1, assessment2])
            db.session.flush()
            
            # Create performance records
            record1 = PerformanceRecord(
                marks_obtained=85.0,
                raw_data_from_excel={"test": "data1"},
                student_id=student.id,
                assessment_id=assessment1.id
            )
            record2 = PerformanceRecord(
                marks_obtained=42.0,
                raw_data_from_excel={"test": "data2"},
                student_id=student.id,
                assessment_id=assessment2.id
            )
            db.session.add_all([record1, record2])
            db.session.commit()
            
            # Make GET request
            response = client.get(f'/api/v1/students/{student.id}/performance')
            
            # Assert response
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            assert response_data['success'] == True
            assert 'data' in response_data
            
            data = response_data['data']
            
            # Check student info structure
            assert 'student_info' in data
            student_info = data['student_info']
            assert student_info['student_roll_number'] == 'CS001'
            assert student_info['first_name'] == 'John'
            assert student_info['last_name'] == 'Doe'
            assert student_info['full_name'] == 'John Doe'
            
            # Check performance summary
            assert 'performance_summary' in data
            summary = data['performance_summary']
            assert summary['total_assessments'] == 2
            assert 'overall_average' in summary
            assert 'overall_grade' in summary
            assert summary['subjects_count'] == 1
            
            # Check subjects performance
            assert 'subjects_performance' in data
            subjects = data['subjects_performance']
            assert 'Mathematics' in subjects
            
            math_data = subjects['Mathematics']
            assert 'assessments' in math_data
            assert len(math_data['assessments']) == 2
            assert 'statistics' in math_data
            
            # Check assessment details
            assessments = math_data['assessments']
            assessment_names = [a['assessment_name'] for a in assessments]
            assert 'Mid-term Exam' in assessment_names
            assert 'Unit Test 1' in assessment_names
            
            # Check assessment timeline
            assert 'assessment_timeline' in data
            timeline = data['assessment_timeline']
            assert len(timeline) == 2
            
            # Check performance trends
            assert 'performance_trends' in data
            trends = data['performance_trends']
            assert 'Mathematics' in trends
            
            # Check insights
            assert 'insights' in data
            insights = data['insights']
            assert 'strongest_subject' in insights
            assert 'weakest_subject' in insights
    
    def test_student_performance_endpoint_not_found(self, client):
        """Test student performance endpoint with non-existent student"""
        # Use a random UUID that doesn't exist
        fake_uuid = "12345678-1234-5678-9012-123456789012"
        
        response = client.get(f'/api/v1/students/{fake_uuid}/performance')
        
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert response_data['success'] == False
        assert 'student not found' in response_data['error'].lower()
    
    def test_student_performance_endpoint_no_data(self, client, app):
        """Test student performance endpoint with student who has no performance data"""
        with app.app_context():
            # Create student with no performance records
            student = Student(
                first_name="Jane",
                last_name="Smith",
                student_roll_number="CS002"
            )
            db.session.add(student)
            db.session.commit()
            
            response = client.get(f'/api/v1/students/{student.id}/performance')
            
            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert response_data['success'] == True
            
            data = response_data['data']
            assert data['performance_summary']['total_assessments'] == 0
            assert data['performance_summary']['overall_average'] == 0
            assert data['performance_summary']['subjects_count'] == 0
            assert len(data['subjects_performance']) == 0
    
    def test_class_overview_endpoint(self, client, app):
        """Test class overview endpoint"""
        with app.app_context():
            # Create comprehensive test data
            subject1 = Subject(subject_name="Mathematics")
            subject2 = Subject(subject_name="Physics")
            db.session.add_all([subject1, subject2])
            db.session.flush()
            
            students = [
                Student(first_name="John", last_name="Doe", student_roll_number="CS001"),
                Student(first_name="Jane", last_name="Smith", student_roll_number="CS002"),
                Student(first_name="Bob", last_name="Johnson", student_roll_number="CS003")
            ]
            db.session.add_all(students)
            db.session.flush()
            
            assessments = [
                Assessment(assessment_name="Math Mid-term", assessment_date=date(2024, 1, 15), 
                          max_marks=100, subject_id=subject1.id),
                Assessment(assessment_name="Physics Mid-term", assessment_date=date(2024, 1, 20), 
                          max_marks=100, subject_id=subject2.id)
            ]
            db.session.add_all(assessments)
            db.session.flush()
            
            # Create performance records
            records = []
            for student in students:
                for assessment in assessments:
                    records.append(PerformanceRecord(
                        marks_obtained=80.0 + (student.id % 20),  # Vary scores
                        student_id=student.id,
                        assessment_id=assessment.id
                    ))
            db.session.add_all(records)
            db.session.commit()
            
            response = client.get('/api/v1/class/overview')
            
            assert response.status_code == 200
            response_data = json.loads(response.data)
            assert response_data['success'] == True
            
            data = response_data['data']
            
            # Check statistics
            assert 'statistics' in data
            stats = data['statistics']
            assert stats['total_students'] == 3
            assert stats['total_subjects'] == 2
            assert stats['total_assessments'] == 2
            assert stats['total_records'] == 6
            
            # Check subjects performance
            assert 'subjects_performance' in data
            subjects = data['subjects_performance']
            assert len(subjects) == 2
            
            # Check grade distribution
            assert 'grade_distribution' in data
            grades = data['grade_distribution']
            assert all(grade in grades for grade in ['A+', 'A', 'B+', 'B', 'C', 'D', 'F'])
            
            # Check charts data
            assert 'charts_data' in data
            charts = data['charts_data']
            assert 'subject_averages' in charts
            assert 'grade_distribution' in charts
    
    def test_student_search_endpoint(self, client, app):
        """Test student search endpoint"""
        with app.app_context():
            # Create test students
            students = [
                Student(first_name="John", last_name="Doe", student_roll_number="CS001"),
                Student(first_name="Jane", last_name="Smith", student_roll_number="CS002"),
                Student(first_name="Johnny", last_name="Johnson", student_roll_number="EE001"),
                Student(first_name="Alice", last_name="Brown", student_roll_number="ME001")
            ]
            db.session.add_all(students)
            db.session.commit()
            
            # Test search by first name
            response = client.get('/api/v1/students?search=John')
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            assert response_data['success'] == True
            
            data = response_data['data']
            assert 'students' in data
            students_found = data['students']
            assert len(students_found) >= 2  # Should find John and Johnny
            
            # Test search by roll number
            response = client.get('/api/v1/students?search=CS001')
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            students_found = response_data['data']['students']
            assert len(students_found) == 1
            assert students_found[0]['student_roll_number'] == 'CS001'
            
            # Test empty search (should return all students)
            response = client.get('/api/v1/students')
            assert response.status_code == 200
            
            response_data = json.loads(response.data)
            students_found = response_data['data']['students']
            assert len(students_found) == 4
            
            # Check pagination info
            assert 'pagination' in response_data['data']
            pagination = response_data['data']['pagination']
            assert 'page' in pagination
            assert 'total' in pagination
            assert pagination['total'] == 4
    
    def test_api_error_handling(self, client):
        """Test API error handling for invalid requests"""
        # Test invalid endpoint
        response = client.get('/api/v1/nonexistent')
        assert response.status_code == 404
        
        # Test invalid student ID format
        response = client.get('/api/v1/students/invalid-uuid/performance')
        assert response.status_code == 404
        
        # Test malformed request data
        response = client.post('/api/v1/upload/subject', data={})
        assert response.status_code == 400