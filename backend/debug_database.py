#!/usr/bin/env python3
"""
Debug script to check database contents
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Student, Subject, Assessment, PerformanceRecord

def debug_database():
    app = create_app()
    
    with app.app_context():
        print("=== DATABASE DEBUG INFO ===")
        
        # Count records
        student_count = db.session.query(Student).count()
        subject_count = db.session.query(Subject).count()
        assessment_count = db.session.query(Assessment).count()
        performance_count = db.session.query(PerformanceRecord).count()
        
        print(f"Students: {student_count}")
        print(f"Subjects: {subject_count}")
        print(f"Assessments: {assessment_count}")
        print(f"Performance Records: {performance_count}")
        
        print("\n=== RECENT STUDENTS ===")
        recent_students = db.session.query(Student).order_by(Student.created_at.desc()).limit(5).all()
        for student in recent_students:
            print(f"- {student.first_name} {student.last_name} ({student.student_roll_number})")
        
        print("\n=== RECENT SUBJECTS ===")
        recent_subjects = db.session.query(Subject).order_by(Subject.created_at.desc()).limit(5).all()
        for subject in recent_subjects:
            print(f"- {subject.subject_name} (Year: {subject.year}, Section: {subject.section})")
        
        print("\n=== RECENT ASSESSMENTS ===")
        recent_assessments = db.session.query(Assessment).order_by(Assessment.created_at.desc()).limit(5).all()
        for assessment in recent_assessments:
            print(f"- {assessment.assessment_name} (Max: {assessment.max_marks})")
        
        print("\n=== RECENT PERFORMANCE RECORDS ===")
        recent_records = db.session.query(PerformanceRecord).order_by(PerformanceRecord.created_at.desc()).limit(10).all()
        for record in recent_records:
            print(f"- Student: {record.student.student_roll_number if record.student else 'Unknown'}, "
                  f"Assessment: {record.assessment.assessment_name if record.assessment else 'Unknown'}, "
                  f"Score: {record.marks_obtained}")
        
        print("\n=== SUBJECT AVERAGES ===")
        from sqlalchemy import func
        subject_averages = db.session.query(
            Subject.subject_name,
            func.avg(PerformanceRecord.marks_obtained).label('avg_marks'),
            func.count(PerformanceRecord.id).label('total_records')
        ).join(
            Assessment, Subject.id == Assessment.subject_id
        ).join(
            PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
        ).group_by(
            Subject.id, Subject.subject_name
        ).all()
        
        for avg in subject_averages:
            print(f"- {avg.subject_name}: {avg.avg_marks:.2f} avg ({avg.total_records} records)")

if __name__ == '__main__':
    debug_database()