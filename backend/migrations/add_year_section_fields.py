"""
Database migration script to add year and section fields to existing tables
Run this script to update your database schema for the college structure
"""

from app import create_app, db
from app.models.performance_models import Subject, Assessment
from sqlalchemy import text

def migrate_database():
    """Add year and section fields to existing tables"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add new columns to subjects table
            print("Adding new columns to subjects table...")
            
            # Check if columns already exist
            result = db.engine.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'subjects' AND column_name IN ('base_subject_name', 'year', 'section')
            """))
            existing_columns = [row[0] for row in result]
            
            if 'base_subject_name' not in existing_columns:
                db.engine.execute(text("ALTER TABLE subjects ADD COLUMN base_subject_name VARCHAR(100)"))
                print("Added base_subject_name column to subjects table")
            
            if 'year' not in existing_columns:
                db.engine.execute(text("ALTER TABLE subjects ADD COLUMN year INTEGER"))
                print("Added year column to subjects table")
            
            if 'section' not in existing_columns:
                db.engine.execute(text("ALTER TABLE subjects ADD COLUMN section VARCHAR(10)"))
                print("Added section column to subjects table")
            
            # Add new columns to assessments table
            print("Adding new columns to assessments table...")
            
            result = db.engine.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'assessments' AND column_name IN ('assessment_type', 'year', 'section')
            """))
            existing_columns = [row[0] for row in result]
            
            if 'assessment_type' not in existing_columns:
                db.engine.execute(text("ALTER TABLE assessments ADD COLUMN assessment_type VARCHAR(50)"))
                print("Added assessment_type column to assessments table")
            
            if 'year' not in existing_columns:
                db.engine.execute(text("ALTER TABLE assessments ADD COLUMN year INTEGER"))
                print("Added year column to assessments table")
            
            if 'section' not in existing_columns:
                db.engine.execute(text("ALTER TABLE assessments ADD COLUMN section VARCHAR(10)"))
                print("Added section column to assessments table")
            
            # Update existing subjects to extract year and section from subject_name if possible
            print("Updating existing subjects...")
            subjects = Subject.query.all()
            for subject in subjects:
                if not subject.base_subject_name and subject.subject_name:
                    # Try to extract base subject name from full name
                    # Example: "Mathematics - Year 2 CSEA" -> base_subject_name="Mathematics", year=2, section="CSEA"
                    if " - Year " in subject.subject_name:
                        parts = subject.subject_name.split(" - Year ")
                        subject.base_subject_name = parts[0]
                        
                        if len(parts) > 1:
                            year_section = parts[1].strip()
                            # Extract year (first character should be the year)
                            if year_section[0].isdigit():
                                subject.year = int(year_section[0])
                                # Extract section (everything after the year and space)
                                section_part = year_section[1:].strip()
                                if section_part:
                                    subject.section = section_part
                    else:
                        # If no pattern found, use the full name as base subject name
                        subject.base_subject_name = subject.subject_name
            
            # Update existing assessments
            print("Updating existing assessments...")
            assessments = Assessment.query.all()
            for assessment in assessments:
                if not assessment.assessment_type:
                    # Set default assessment type
                    assessment.assessment_type = "General Assessment"
                
                # Try to extract year and section from assessment_name if possible
                if assessment.subject and assessment.subject.year:
                    assessment.year = assessment.subject.year
                if assessment.subject and assessment.subject.section:
                    assessment.section = assessment.subject.section
            
            # Commit all changes
            db.session.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate_database()