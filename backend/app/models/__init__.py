# Converted to a package for future scalability
from .performance_models import Student, Subject, Assessment, PerformanceRecord
from .user_models import UserManager

__all__ = ['Student', 'Subject', 'Assessment', 'PerformanceRecord', 'UserManager']