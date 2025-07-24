import pytest
import tempfile
import os
from app import create_app, db
from app.models import Student, Subject, Assessment, PerformanceRecord

@pytest.fixture
def app():
    """Create and configure a test app instance"""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Create app with test configuration
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    # Create application context
    with test_app.app_context():
        # Create all database tables
        db.create_all()
        yield test_app
        
        # Clean up
        db.drop_all()
    
    # Close and remove temporary database file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client for making requests"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def sample_student(app):
    """Create a sample student for testing"""
    with app.app_context():
        student = Student(
            first_name="John",
            last_name="Doe",
            student_roll_number="CS001"
        )
        db.session.add(student)
        db.session.commit()
        return student

@pytest.fixture
def sample_subject(app):
    """Create a sample subject for testing"""
    with app.app_context():
        subject = Subject(subject_name="Mathematics")
        db.session.add(subject)
        db.session.commit()
        return subject

@pytest.fixture
def sample_assessment(app, sample_subject):
    """Create a sample assessment for testing"""
    with app.app_context():
        assessment = Assessment(
            assessment_name="Mid-term Exam",
            assessment_date="2024-01-15",
            max_marks=100,
            subject_id=sample_subject.id
        )
        db.session.add(assessment)
        db.session.commit()
        return assessment

@pytest.fixture
def sample_performance_record(app, sample_student, sample_assessment):
    """Create a sample performance record for testing"""
    with app.app_context():
        record = PerformanceRecord(
            marks_obtained=85.5,
            raw_data_from_excel={"test": "data"},
            student_id=sample_student.id,
            assessment_id=sample_assessment.id
        )
        db.session.add(record)
        db.session.commit()
        return record

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
    }