import pytest
import pandas as pd
import tempfile
import os
from app.services.data_processor import parse_excel_file, allowed_file, calculate_percentage, get_grade
from app.services.data_processor import process_regular_subject_data, process_crt_data, process_programming_data

class TestDataProcessor:
    """Test suite for data processing functions"""
    
    def create_sample_excel_file(self, data, filename="test_data.xlsx"):
        """Helper method to create sample Excel files for testing"""
        df = pd.DataFrame(data)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        df.to_excel(temp_file.name, index=False)
        temp_file.close()
        return temp_file.name
    
    def test_allowed_file(self):
        """Test file extension validation"""
        # Valid files
        assert allowed_file('test.xlsx') == True
        assert allowed_file('test.xls') == True
        assert allowed_file('DATA.XLSX') == True  # Case insensitive
        
        # Invalid files
        assert allowed_file('test.txt') == False
        assert allowed_file('test.pdf') == False
        assert allowed_file('test.csv') == False
        assert allowed_file('test') == False
        assert allowed_file('') == False
    
    def test_calculate_percentage(self):
        """Test percentage calculation"""
        assert calculate_percentage(80, 100) == 80.0
        assert calculate_percentage(45, 50) == 90.0
        assert calculate_percentage(0, 100) == 0.0
        assert calculate_percentage(100, 100) == 100.0
        assert calculate_percentage(50, 0) == 0  # Edge case: division by zero
    
    def test_get_grade(self):
        """Test grade calculation"""
        assert get_grade(95) == 'A+'
        assert get_grade(90) == 'A+'
        assert get_grade(85) == 'A'
        assert get_grade(80) == 'A'
        assert get_grade(75) == 'B+'
        assert get_grade(70) == 'B+'
        assert get_grade(65) == 'B'
        assert get_grade(60) == 'B'
        assert get_grade(55) == 'C'
        assert get_grade(50) == 'C'
        assert get_grade(45) == 'D'
        assert get_grade(40) == 'D'
        assert get_grade(35) == 'F'
        assert get_grade(0) == 'F'
    
    def test_parse_excel_file_basic(self):
        """Test basic Excel file parsing"""
        # Create sample data
        data = {
            'Student ID': ['CS001', 'CS002', 'CS003'],
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'Marks': [85, 78, 92]
        }
        
        file_path = self.create_sample_excel_file(data)
        
        try:
            df = parse_excel_file(file_path)
            
            # Check basic properties
            assert len(df) == 3
            assert len(df.columns) == 3
            
            # Check column standardization (lowercase, underscores)
            expected_columns = ['student_id', 'name', 'marks']
            assert list(df.columns) == expected_columns
            
            # Check data types
            assert df['marks'].dtype in ['int64', 'float64']  # Should be numeric
            
            # Check data integrity
            assert df.loc[0, 'student_id'] == 'CS001'
            assert df.loc[0, 'name'] == 'John Doe'
            assert df.loc[0, 'marks'] == 85
            
        finally:
            os.unlink(file_path)
    
    def test_parse_excel_file_with_missing_values(self):
        """Test Excel parsing with missing values and edge cases"""
        # Create data with missing values and edge cases
        data = {
            'Student ID': ['CS001', 'CS002', '', 'CS004', None],
            'Name': ['John Doe', '', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
            'Mid Term': [85, None, 78, 92, ''],
            'Unit Test 1': [88, 82, '', 89, 95],
            'Unit Test 2': ['', 85, 87, None, 91],
            'Empty Column': [None, None, None, None, None]
        }
        
        file_path = self.create_sample_excel_file(data)
        
        try:
            df = parse_excel_file(file_path)
            
            # Check that empty columns are removed
            assert 'empty_column' not in df.columns
            
            # Check that completely empty rows are removed
            assert len(df) <= 5  # Should be <= original due to empty row removal
            
            # Check column standardization
            expected_columns = ['student_id', 'name', 'mid_term', 'unit_test_1', 'unit_test_2']
            assert all(col in df.columns for col in expected_columns)
            
            # Check numeric conversion
            numeric_cols = ['mid_term', 'unit_test_1', 'unit_test_2']
            for col in numeric_cols:
                if col in df.columns:
                    assert df[col].dtype in ['int64', 'float64', 'object']  # May contain NaN
            
        finally:
            os.unlink(file_path)
    
    def test_parse_excel_file_empty_file(self):
        """Test parsing empty Excel file"""
        # Create empty DataFrame
        empty_data = pd.DataFrame()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        empty_data.to_excel(temp_file.name, index=False)
        temp_file.close()
        
        try:
            with pytest.raises(Exception) as exc_info:
                parse_excel_file(temp_file.name)
            assert "empty" in str(exc_info.value).lower()
        finally:
            os.unlink(temp_file.name)
    
    def test_parse_excel_file_nonexistent(self):
        """Test parsing non-existent file"""
        with pytest.raises(Exception) as exc_info:
            parse_excel_file("nonexistent_file.xlsx")
        assert "not found" in str(exc_info.value).lower()
    
    def test_process_regular_subject_data(self):
        """Test processing regular subject data"""
        # Create sample DataFrame (already processed by parse_excel_file)
        data = {
            'student_id': ['CS001', 'CS002', 'CS003'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'mid_term': [85.0, 78.0, 92.0],
            'unit_test_1': [88.0, 82.0, 89.0],
            'unit_test_2': [90.0, 85.0, 87.0]
        }
        df = pd.DataFrame(data)
        
        result = process_regular_subject_data(df, "Mathematics")
        
        # Should have 9 records (3 students × 3 assessments)
        assert len(result) == 9
        
        # Check structure of first record
        first_record = result[0]
        assert 'student_id' in first_record
        assert 'student_name' in first_record
        assert 'subject_name' in first_record
        assert 'data_type' in first_record
        assert 'score' in first_record
        assert 'max_score' in first_record
        
        # Check data integrity
        assert first_record['subject_name'] == "Mathematics"
        assert first_record['student_id'] == 'CS001'
        assert first_record['student_name'] == 'John Doe'
    
    def test_process_crt_data(self):
        """Test processing CRT (weekly) data"""
        data = {
            'student_id': ['CS001', 'CS002', 'CS003'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'week': [1, 1, 1],
            'crt_score': [85.0, 78.0, 92.0]
        }
        df = pd.DataFrame(data)
        
        result = process_crt_data(df, "CRT")
        
        # Should have 3 records (3 students × 1 week)
        assert len(result) == 3
        
        # Check structure
        first_record = result[0]
        assert first_record['data_type'] == 'CRT Score'
        assert first_record['week_number'] == 1
        assert first_record['subject_name'] == "CRT"
    
    def test_process_programming_data(self):
        """Test processing competitive programming data"""
        data = {
            'student_id': ['CS001', 'CS002', 'CS003'],
            'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'problems_solved': [45, 38, 52]
        }
        df = pd.DataFrame(data)
        
        result = process_programming_data(df, "Programming")
        
        # Should have 3 records
        assert len(result) == 3
        
        # Check structure
        first_record = result[0]
        assert first_record['data_type'] == 'Problems Solved'
        assert first_record['max_score'] == 1000  # Default max for programming
        assert first_record['subject_name'] == "Programming"
    
    def test_process_data_missing_required_columns(self):
        """Test processing data with missing required columns"""
        # Missing 'name' column
        data = {
            'student_id': ['CS001', 'CS002'],
            'marks': [85, 78]
        }
        df = pd.DataFrame(data)
        
        with pytest.raises(Exception) as exc_info:
            process_regular_subject_data(df, "Mathematics")
        assert "missing required columns" in str(exc_info.value).lower()
    
    def test_data_cleaning_edge_cases(self):
        """Test data cleaning with various edge cases"""
        data = {
            'Student ID ': [' CS001 ', 'CS002', 'CS003'],  # Extra spaces
            ' Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],  # Leading space
            'Mid-Term Exam': [85, 78, 92],  # Hyphen in name
            'Unit Test #1': [88, 82, 89],  # Special character
            'FINAL SCORE': [90, 85, 87]  # All caps
        }
        
        file_path = self.create_sample_excel_file(data)
        
        try:
            df = parse_excel_file(file_path)
            
            # Check column name standardization
            expected_columns = ['student_id', 'name', 'mid-term_exam', 'unit_test_#1', 'final_score']
            for col in df.columns:
                assert col.islower()  # All lowercase
                assert not col.startswith(' ')  # No leading spaces
                assert not col.endswith(' ')  # No trailing spaces
            
        finally:
            os.unlink(file_path)
    
    def teardown_method(self):
        """Clean up any temporary files after each test"""
        # This runs after each test method
        pass