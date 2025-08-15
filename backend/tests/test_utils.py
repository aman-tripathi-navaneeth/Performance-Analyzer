import unittest
import pandas as pd
import tempfile
import os
from app.utils import process_excel_file, calculate_percentage, get_grade, allowed_file

class TestUtils(unittest.TestCase):
    
    def test_allowed_file(self):
        """Test file extension validation"""
        self.assertTrue(allowed_file('test.xlsx'))
        self.assertTrue(allowed_file('test.xls'))
        self.assertFalse(allowed_file('test.txt'))
        self.assertFalse(allowed_file('test.pdf'))
        self.assertFalse(allowed_file('test'))
    
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        self.assertEqual(calculate_percentage(80, 100), 80.0)
        self.assertEqual(calculate_percentage(45, 50), 90.0)
        self.assertEqual(calculate_percentage(0, 100), 0.0)
        self.assertEqual(calculate_percentage(100, 0), 0)  # Edge case
    
    def test_get_grade(self):
        """Test grade calculation"""
        self.assertEqual(get_grade(95), 'A+')
        self.assertEqual(get_grade(85), 'A')
        self.assertEqual(get_grade(75), 'B+')
        self.assertEqual(get_grade(65), 'B')
        self.assertEqual(get_grade(55), 'C')
        self.assertEqual(get_grade(45), 'D')
        self.assertEqual(get_grade(35), 'F')
    
    def test_process_regular_subject_data(self):
        """Test processing regular subject Excel data"""
        # Create sample data
        data = {
            'Student ID': ['S001', 'S002', 'S003'],
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'Mid-term': [85, 78, 92],
            'Unit Test 1': [88, 82, 89],
            'Unit Test 2': [90, 85, 87]
        }
        df = pd.DataFrame(data)
        
        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            df.to_excel(tmp.name, index=False)
            
            # Process the file
            result = process_excel_file(tmp.name, 'Mathematics', 'regular')
            
            # Clean up
            os.unlink(tmp.name)
        
        # Verify results
        self.assertEqual(len(result), 9)  # 3 students × 3 assessments
        self.assertEqual(result[0]['student_id'], 'S001')
        self.assertEqual(result[0]['student_name'], 'John Doe')
        self.assertEqual(result[0]['subject_name'], 'Mathematics')

if __name__ == '__main__':
    unittest.main()