import sqlite3

def upgrade_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE student_performance ADD COLUMN normalized_score FLOAT")
    except sqlite3.OperationalError:
        pass # Column might exist
        
    try:
        cursor.execute("ALTER TABLE student_performance ADD COLUMN assessment_score FLOAT")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE student_performance ADD COLUMN final_combined_score FLOAT")
    except sqlite3.OperationalError:
        pass
        
    try:
        cursor.execute("ALTER TABLE student_performance ADD COLUMN performance_category VARCHAR")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    upgrade_db()
