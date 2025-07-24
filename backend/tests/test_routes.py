import unittest
import json
import tempfile
import os
from app import create_app
from app.models import DatabaseManager

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Use temporary database for testing
        self.app.config['DATABASE_PATH'] = ':memory:'
        
        with self.app.app_context():
            db = DatabaseManager()
            db.init_database()
    
    def test_get_all_students_empty(self):
        """Test getting students when database is empty"""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['students'], [])
    
    def test_get_subjects_empty(self):
        """Test getting subjects when database is empty"""
        response = self.client.get('/api/uploads/subjects')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['subjects'], [])
    
    def test_search_students_empty_query(self):
        """Test searching students with empty query"""
        response = self.client.get('/api/students/search?q=')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['students'], [])
    
    def test_get_class_performance_empty(self):
        """Test getting class performance when no data exists"""
        response = self.client.get('/api/analytics/class-performance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['subjects_performance'], [])
        self.assertEqual(data['overall_class_average'], 0)
    
    def test_get_statistics_empty(self):
        """Test getting statistics when database is empty"""
        response = self.client.get('/api/analytics/statistics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_students'], 0)
        self.assertEqual(data['total_subjects'], 0)
        self.assertEqual(data['total_records'], 0)
    
    def test_upload_file_no_file(self):
        """Test file upload without providing a file"""
        response = self.client.post('/api/uploads/upload')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_upload_file_no_subject_name(self):
        """Test file upload without subject name"""
        data = {'file': (tempfile.NamedTemporaryFile(suffix='.xlsx'), 'test.xlsx')}
        response = self.client.post('/api/uploads/upload', data=data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()