#!/usr/bin/env python3

import re

def fix_analytics_file():
    """Add year_section_distribution to the analytics.py file"""
    
    # Read the current file
    with open('app/api/analytics.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the overview_data definition and add year_section_distribution
    # Look for the pattern where overview_data is defined
    pattern = r"(overview_data = \{[^}]*'year_distribution': year_distribution,)"
    
    replacement = r"\1\n            'year_section_distribution': year_section_distribution,"
    
    # Check if year_section_distribution is already there
    if 'year_section_distribution' in content:
        print("✅ year_section_distribution already exists in the file")
        return
    
    # Add the year_section_distribution calculation before overview_data
    # Find where year_distribution is calculated
    year_dist_pattern = r"(year_distribution\[year_mapping\[year_count\.year\]\] = year_count\.student_count)"
    
    year_section_code = '''
        # Get year/section distribution
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
        
        # Process year/section data
        year_section_distribution = {}
        
        # Process year/section data
        for record in year_section_counts:
            if record.year in year_mapping:
                year_label = year_mapping[record.year]
                
                # Initialize year in distribution if not exists
                if year_label not in year_section_distribution:
                    year_section_distribution[year_label] = {}
                
                # Add section data (accumulate if section already exists)
                if record.section in year_section_distribution[year_label]:
                    year_section_distribution[year_label][record.section] += record.student_count
                else:
                    year_section_distribution[year_label][record.section] = record.student_count
'''
    
    # Add the year_section calculation after year_distribution calculation
    content = re.sub(year_dist_pattern, r"\1" + year_section_code, content)
    
    # Add year_section_distribution to the overview_data
    content = re.sub(pattern, replacement, content)
    
    # Write the updated content back
    with open('app/api/analytics.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added year_section_distribution to analytics.py")

if __name__ == "__main__":
    fix_analytics_file()