import sqlite3

def patch_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    try:
        # Update years
        cursor.execute("UPDATE student_performance SET year = 'First Year' WHERE year = '1'")
        cursor.execute("UPDATE student_performance SET year = 'Second Year' WHERE year = '2'")
        cursor.execute("UPDATE student_performance SET year = 'Third Year' WHERE year = '3'")
        cursor.execute("UPDATE student_performance SET year = 'Fourth Year' WHERE year = '4'")

        # Update branches
        cursor.execute("UPDATE student_performance SET branch = 'MECH' WHERE branch = 'MEC'")
        cursor.execute("UPDATE student_performance SET branch = 'CSM' WHERE branch = 'CSC'")
        
        conn.commit()
        print("Successfully updated database records.")
    except sqlite3.Error as e:
        print(f"Error updating DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    patch_db()
