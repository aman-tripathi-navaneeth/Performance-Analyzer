#!/usr/bin/env python3
"""
Debug the analytics API to see what's happening with year_section_distribution
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Student, Subject, Assessment, PerformanceRecord
from sqlalchemy import func

def debug_analytics_api():
    """Debug the analytics API year/section logic"""
    app = create_app()
    
    with app.app_context():
        print("=== DEBUGGING ANALYTICS API YEAR/SECTION LOGIC ===")
        
        # Same query as in analytics.py
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
        
        print(f"\nQuery Results ({len(year_section_counts)} records):")
        for record in year_section_counts:
            print(f"  Year {record.year}, Section {record.section}: {record.student_count} students")
        
        # Same processing logic as analytics.py
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
        
        print(f"\nProcessing records...")
        for record in year_section_counts:
            print(f"  Processing: Year {record.year}, Section {record.section}, Count {record.student_count}")
            if record.year in year_mapping:
                year_label = year_mapping[record.year]
                print(f"    -> Mapped to: {year_label}")
                
                if year_label not in year_section_distribution:
                    year_section_distribution[year_label] = {}
                    print(f"    -> Initialized {year_label} in distribution")
                
                year_section_distribution[year_label][record.section] = record.student_count
                print(f"    -> Added {record.section}: {record.student_count} to {year_label}")
                
                year_distribution[year_label] += record.student_count
                print(f"    -> Updated {year_label} total to {year_distribution[year_label]}")
            else:
                print(f"    -> Year {record.year} not in mapping, skipping")
        
        print(f"\nFinal year_section_distribution:")
        print(f"  {year_section_distribution}")
        
        print(f"\nFinal year_distribution:")
        print(f"  {year_distribution}")
        
        # Test if it's empty
        if not year_section_distribution:
            print(f"\n❌ year_section_distribution is EMPTY!")
        else:
            print(f"\n✅ year_section_distribution has data")

if __name__ == "__main__":
    debug_analytics_api()