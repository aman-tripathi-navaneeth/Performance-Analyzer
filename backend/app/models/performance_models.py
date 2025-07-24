from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    student_roll_number = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name} - {self.student_roll_number}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_roll_number': self.student_roll_number,
            'full_name': f'{self.first_name} {self.last_name}',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_name = db.Column(db.String(200), nullable=False)
    base_subject_name = db.Column(db.String(100), nullable=True)  # e.g., "Mathematics"
    year = db.Column(db.Integer, nullable=True)  # 1, 2, 3, 4
    section = db.Column(db.String(10), nullable=True)  # CSEA, CSEB, CSM, ECE, COS
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Add unique constraint for subject_name OR combination of base_subject_name, year, section
    __table_args__ = (
        db.UniqueConstraint('base_subject_name', 'year', 'section', name='unique_subject_year_section'),
    )
    
    def __repr__(self):
        return f'<Subject {self.subject_name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'subject_name': self.subject_name,
            'base_subject_name': self.base_subject_name,
            'year': self.year,
            'section': self.section,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_name = db.Column(db.String(200), nullable=False)
    assessment_date = db.Column(db.Date, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    assessment_type = db.Column(db.String(50), nullable=True)  # Mid-term, Final, Quiz, etc.
    year = db.Column(db.Integer, nullable=True)  # 1, 2, 3, 4
    section = db.Column(db.String(10), nullable=True)  # CSEA, CSEB, CSM, ECE, COS
    subject_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subjects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship
    subject = db.relationship('Subject', backref=db.backref('assessments', lazy=True))
    
    def __repr__(self):
        return f'<Assessment {self.assessment_name} - {self.subject.subject_name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'assessment_name': self.assessment_name,
            'assessment_date': self.assessment_date.isoformat() if self.assessment_date else None,
            'max_marks': self.max_marks,
            'assessment_type': self.assessment_type,
            'year': self.year,
            'section': self.section,
            'subject_id': str(self.subject_id),
            'subject_name': self.subject.subject_name if self.subject else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PerformanceRecord(db.Model):
    __tablename__ = 'performance_records'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    marks_obtained = db.Column(db.Float, nullable=False)
    raw_data_from_excel = db.Column(JSONB, nullable=True)
    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('students.id'), nullable=False)
    assessment_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assessments.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    student = db.relationship('Student', backref=db.backref('performance_records', lazy=True))
    assessment = db.relationship('Assessment', backref=db.backref('performance_records', lazy=True))
    
    def __repr__(self):
        return f'<PerformanceRecord {self.student.student_roll_number} - {self.assessment.assessment_name}: {self.marks_obtained}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'marks_obtained': self.marks_obtained,
            'percentage': (self.marks_obtained / self.assessment.max_marks * 100) if self.assessment and self.assessment.max_marks > 0 else 0,
            'raw_data_from_excel': self.raw_data_from_excel,
            'student_id': str(self.student_id),
            'assessment_id': str(self.assessment_id),
            'student_name': f'{self.student.first_name} {self.student.last_name}' if self.student else None,
            'student_roll_number': self.student.student_roll_number if self.student else None,
            'assessment_name': self.assessment.assessment_name if self.assessment else None,
            'max_marks': self.assessment.max_marks if self.assessment else None,
            'subject_name': self.assessment.subject.subject_name if self.assessment and self.assessment.subject else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }