#!/usr/bin/env python3
"""
Debug year/section distribution
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app import db
from app.models import Subject, Assessment, PerformanceRecord
from sqlalchemy import func

def debug_year_section():
    """Debug year/section data"""
    app = create_app()
    
    with app.app_context():
        print("=== DEBUGGING YEAR/SECTION DISTRIBUTION ===")
        
        # Check what year/section data exists
        year_section_counts = db.session.query(
            Subject.year,
            Subject.section,
            func.count(func.distinct(PerformanceRecord.student_id)).label('student_count')
        ).join(
            Assessment, Subject.id == Assessment.subject_id
        ).join(
            PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
        ).filter(
            Subject.year.isnot(None),
            Subject.section.isnot(None)
        ).group_by(
            Subject.year, Subject.section
        ).all()
        
        print(f"Found {len(year_section_counts)} year/section combinations:")
        for record in year_section_counts:
            print(f"  Year {record.year}, Section {record.section}: {record.student_count} students")
        
        # Check subjects with year/section data
        subjects_with_year_section = db.session.query(
            Subject.id,
            Subject.subject_name,
            Subject.year,
            Subject.section
        ).filter(
            Subject.year.isnot(None),
            Subject.section.isnot(None)
        ).all()
        
        print(f"\nSubjects with year/section data ({len(subjects_with_year_section)}):")
        for subject in subjects_with_year_section[:5]:  # Show first 5
            print(f"  - {subject.subject_name} (Year {subject.year}, Section {subject.section})")
        
        # Test the distribution logic
        year_section_distribution = {}
        year_distribution = {
            '1st Year': 0,
            '2nd Year': 0,
            '3rd Year': 0,
            '4th Year': 0
        }
        
        year_mapping = {
            1: '1st Year',
            2: '2nd Year', 
            3: '3rd Year',
            4: '4th Year'
        }
        
        for record in year_section_counts:
            if record.year in year_mapping:
                year_label = year_mapping[record.year]
                
                if year_label not in year_section_distribution:
                    year_section_distribution[year_label] = {}
                
                year_section_distribution[year_label][record.section] = record.student_count
                year_distribution[year_label] += record.student_count
        
        print(f"\nGenerated year_section_distribution:")
        print(f"  {year_section_distribution}")
        
        print(f"\nGenerated year_distribution:")
        print(f"  {year_distribution}")

if __name__ == "__main__":
    debug_year_section()