#!/usr/bin/env python3
"""
Direct test of the upload functionality to debug the issue
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.services.data_processor import parse_excel_file
from app.models.performance_models import Student, Subject, Assessment, PerformanceRecord
import pandas as pd
import json
from datetime import datetime

def test_csv_upload():
    """Test the CSV upload process step by step"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING CSV UPLOAD PROCESS ===")
        
        # Step 1: Parse the CSV file
        csv_path = "../sample_data/Test_Mathematics_Fixed.csv"
        if not os.path.exists(csv_path):
            print(f"ERROR: CSV file not found at {csv_path}")
            return
        
        print(f"1. Parsing CSV file: {csv_path}")
        try:
            df = parse_excel_file(csv_path)
            print(f"   ✓ Successfully parsed CSV")
            print(f"   ✓ Shape: {df.shape}")
            print(f"   ✓ Columns: {list(df.columns)}")
            print(f"   ✓ First 3 rows:")
            for i, row in df.head(3).iterrows():
                print(f"     Row {i}: {dict(row)}")
        except Exception as e:
            print(f"   ✗ Error parsing CSV: {e}")
            return
        
        # Step 2: Test subject creation
        print("\n2. Testing subject creation")
        subject_name = "Mathematics Test"
        year = 2
        section = "CSE A"
        
        subject = Subject.query.filter_by(
            base_subject_name=subject_name,
            year=year,
            section=section
        ).first()
        
        if not subject:
            subject_full_name = f"{subject_name} - Year {year} {section}"
            subject = Subject(
                subject_name=subject_full_name,
                base_subject_name=subject_name,
                year=year,
                section=section
            )
            db.session.add(subject)
            db.session.flush()
            print(f"   ✓ Created new subject: {subject_full_name} (ID: {subject.id})")
        else:
            print(f"   ✓ Using existing subject: {subject.subject_name} (ID: {subject.id})")
        
        # Step 3: Test assessment creation
        print("\n3. Testing assessment creation")
        assessment_type = "General Assessment"
        assessment_name = f"{assessment_type} - {subject_name} (Year {year} {section})"
        assessment_date_obj = datetime.now().date()
        
        assessment = Assessment(
            assessment_name=assessment_name,
            assessment_date=assessment_date_obj,
            max_marks=100,
            subject_id=subject.id,
            year=year,
            section=section,
            assessment_type=assessment_type
        )
        db.session.add(assessment)
        db.session.flush()
        print(f"   ✓ Created assessment: {assessment_name} (ID: {assessment.id})")
        
        # Step 4: Test student and performance record creation
        print("\n4. Testing student and performance record creation")
        students_created = 0
        records_created = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Extract data using the same logic as the upload endpoint
                student_roll_number = str(row.get('student_id', row.get('Student ID', ''))).strip()
                full_name = str(row.get('student_name', row.get('Student Name', ''))).strip()
                marks_obtained = row.get('score', row.get('Score', 0))
                
                print(f"   Processing row {index + 1}:")
                print(f"     ID: '{student_roll_number}'")
                print(f"     Name: '{full_name}'")
                print(f"     Score: '{marks_obtained}'")
                
                if not student_roll_number or not full_name:
                    error = f"Row {index + 1}: Missing ID or name"
                    errors.append(error)
                    print(f"     ✗ {error}")
                    continue
                
                # Parse name
                name_parts = full_name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''
                
                # Find or create student
                student = Student.query.filter_by(student_roll_number=student_roll_number).first()
                if not student:
                    student = Student(
                        first_name=first_name,
                        last_name=last_name,
                        student_roll_number=student_roll_number
                    )
                    db.session.add(student)
                    db.session.flush()
                    students_created += 1
                    print(f"     ✓ Created student: {student_roll_number} - {first_name} {last_name} (ID: {student.id})")
                else:
                    print(f"     ✓ Using existing student: {student_roll_number} (ID: {student.id})")
                
                # Create performance record
                performance_record = PerformanceRecord(
                    marks_obtained=float(marks_obtained),
                    raw_data_from_excel=json.dumps(row.to_dict()),
                    student_id=student.id,
                    assessment_id=assessment.id
                )
                db.session.add(performance_record)
                records_created += 1
                print(f"     ✓ Created performance record: {marks_obtained} marks")
                
            except Exception as row_error:
                error = f"Row {index + 1}: {str(row_error)}"
                errors.append(error)
                print(f"     ✗ {error}")
                continue
        
        # Step 5: Commit changes
        print(f"\n5. Committing changes to database")
        try:
            db.session.commit()
            print(f"   ✓ Successfully committed all changes")
            print(f"   ✓ Students created: {students_created}")
            print(f"   ✓ Performance records created: {records_created}")
            if errors:
                print(f"   ⚠ Errors encountered: {len(errors)}")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"     - {error}")
        except Exception as commit_error:
            print(f"   ✗ Error committing changes: {commit_error}")
            db.session.rollback()
            return
        
        # Step 6: Verify data in database
        print(f"\n6. Verifying data in database")
        total_students = Student.query.count()
        total_subjects = Subject.query.count()
        total_assessments = Assessment.query.count()
        total_records = PerformanceRecord.query.count()
        
        print(f"   ✓ Total students: {total_students}")
        print(f"   ✓ Total subjects: {total_subjects}")
        print(f"   ✓ Total assessments: {total_assessments}")
        print(f"   ✓ Total performance records: {total_records}")
        
        # Show recent students
        recent_students = Student.query.order_by(Student.id.desc()).limit(5).all()
        print(f"   ✓ Recent students:")
        for student in recent_students:
            print(f"     - {student.student_roll_number}: {student.first_name} {student.last_name}")
        
        print("\n=== TEST COMPLETED ===")

if __name__ == "__main__":
    test_csv_upload()