# Performance Analyzer - Backend API

A Flask-based backend system for analyzing student performance across multiple subjects and assessments.

## Features

- **Multi-Subject Analysis**: Upload and process Excel files for different subjects
- **Weekly CRT Integration**: Merge weekly CRT (Coding Round Test) data automatically
- **Individual Student Profiles**: Track each student's performance across all subjects
- **Class Performance Analytics**: View overall class trends and statistics
- **Competitive Programming Tracking**: Monitor problems solved on programming platforms
- **Data Visualization Ready**: APIs designed for frontend chart integration
- **Advanced Analytics**: Identify struggling students and subject difficulty analysis

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes/
│   │   ├── __init__.py      # Route blueprints registration
│   │   ├── students.py      # Student-related endpoints
│   │   ├── uploads.py       # File upload endpoints
│   │   └── analytics.py     # Data analysis endpoints
│   ├── models.py            # Database models and operations
│   ├── utils.py             # Helper functions for data processing
│   ├── services.py          # Business logic layer
│   ├── config.py            # Application configuration
│   └── database.db          # SQLite database (auto-created)
├── uploads/                 # Excel file storage directory
├── tests/                   # Unit and integration tests
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### File Upload
- `POST /api/uploads/upload` - Upload Excel file with student performance data
- `GET /api/uploads/subjects` - Get all subjects

### Student Management
- `GET /api/students/` - Get all students
- `GET /api/students/<student_id>` - Get individual student profile
- `GET /api/students/search?q=<query>` - Search students by name or ID

### Analytics
- `GET /api/analytics/class-performance` - Get overall class performance
- `GET /api/analytics/subject-performance/<subject_id>` - Get subject-specific performance
- `GET /api/analytics/trends` - Get performance trends over time (CRT data)
- `GET /api/analytics/statistics` - Get system statistics and grade distribution

## Excel File Format

### Regular Subjects (Mid-term, Unit Tests)
```
| Student ID | Name        | Mid-term | Unit Test 1 | Unit Test 2 |
|------------|-------------|----------|-------------|-------------|
| S001       | John Doe    | 85       | 88          | 90          |
| S002       | Jane Smith  | 78       | 82          | 85          |
```

### CRT (Weekly Tests)
```
| Student ID | Name        | Week | CRT Score |
|------------|-------------|------|-----------|
| S001       | John Doe    | 1    | 85        |
| S001       | John Doe    | 2    | 88        |
| S002       | Jane Smith  | 1    | 78        |
```

### Competitive Programming
```
| Student ID | Name        | Problems Solved |
|------------|-------------|-----------------|
| S001       | John Doe    | 45              |
| S002       | Jane Smith  | 38              |
```

## Usage Examples

### Upload a File
```bash
curl -X POST \
  http://localhost:5000/api/uploads/upload \
  -F "file=@mathematics_midterm.xlsx" \
  -F "subject_name=Mathematics" \
  -F "subject_type=regular"
```

### Get Student Profile
```bash
curl http://localhost:5000/api/students/S001
```

### Get Class Performance
```bash
curl http://localhost:5000/api/analytics/class-performance
```

## Database Schema

### Students Table
- `id` (Primary Key)
- `student_id` (Unique)
- `name`
- `created_at`

### Subjects Table
- `id` (Primary Key)
- `name`
- `subject_type` (regular/crt/programming)
- `created_at`

### Performance Data Table
- `id` (Primary Key)
- `student_id` (Foreign Key)
- `subject_id` (Foreign Key)
- `data_type` (Mid-term, Unit Test, CRT Score, etc.)
- `score`
- `max_score`
- `week_number` (for CRT data)
- `upload_date`
- `metadata` (JSON for additional data)

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python -m unittest tests.test_utils
python -m unittest tests.test_routes
```

## Configuration

Key configuration options in `app/config.py`:
- `UPLOAD_FOLDER`: Directory for uploaded files
- `MAX_CONTENT_LENGTH`: Maximum file size (16MB)
- `ALLOWED_EXTENSIONS`: Supported file types (.xlsx, .xls)
- `DATABASE_PATH`: SQLite database location

## Error Handling

The API returns consistent error responses:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `500`: Internal Server Error

## Performance Features

1. **Automatic Data Merging**: CRT data is automatically merged with existing weekly data
2. **Grade Calculation**: Automatic grade assignment based on percentage scores
3. **Trend Analysis**: Track student progress over time
4. **Class Comparison**: Rank students within subjects
5. **Difficulty Analysis**: Identify challenging subjects
6. **Struggling Student Detection**: Automatically flag students needing help

## Future Enhancements

- Real-time data updates via WebSocket
- Advanced visualization endpoints
- Export functionality for reports
- Email notifications for performance alerts
- Integration with external learning management systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.