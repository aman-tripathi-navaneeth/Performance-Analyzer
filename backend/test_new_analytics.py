#!/usr/bin/env python3
"""
Test with a completely new analytics implementation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Blueprint, jsonify
from app import create_app, db
from app.models import Student, Subject, Assessment, PerformanceRecord
from sqlalchemy import func

# Create a new blueprint
test_analytics_bp = Blueprint('test_analytics', __name__)

@test_analytics_bp.route('/test-overview', methods=['GET'])
def test_overview():
    """Test overview endpoint"""
    try:
        # Get year/section data
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
        
        # Process data
        year_section_distribution = {}
        year_mapping = {1: '1st Year', 2: '2nd Year', 3: '3rd Year', 4: '4th Year'}
        
        for record in year_section_counts:
            if record.year in year_mapping:
                year_label = year_mapping[record.year]
                if year_label not in year_section_distribution:
                    year_section_distribution[year_label] = {}
                year_section_distribution[year_label][record.section] = record.student_count
        
        return jsonify({
            'success': True,
            'data': {
                'year_section_distribution': year_section_distribution,
                'raw_counts': [{'year': r.year, 'section': r.section, 'count': r.student_count} for r in year_section_counts]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def test_new_analytics():
    """Test the new analytics"""
    app = create_app()
    
    # Register the test blueprint
    app.register_blueprint(test_analytics_bp, url_prefix='/api/v1/test')
    
    with app.app_context():
        with app.test_client() as client:
            response = client.get('/api/v1/test/test-overview')
            print(f"Status: {response.status_code}")
            data = response.get_json()
            print(f"Success: {data.get('success', False)}")
            
            if data.get('success'):
                overview_data = data['data']
                print(f"Keys: {list(overview_data.keys())}")
                
                if 'year_section_distribution' in overview_data:
                    print(f"✅ year_section_distribution found!")
                    print(f"Content: {overview_data['year_section_distribution']}")
                else:
                    print(f"❌ year_section_distribution not found!")
                    
                print(f"Raw counts: {overview_data.get('raw_counts', [])}")
            else:
                print(f"Error: {data.get('error', 'Unknown')}")

if __name__ == "__main__":
    test_new_analytics()