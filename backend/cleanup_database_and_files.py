#!/usr/bin/env python3
"""
Comprehensive cleanup script to:
1. Delete all data from the database
2. Remove all CSV/Excel files from sample_data directory
3. Reset the database to a clean state
"""
import os
import sqlite3
import glob
import shutil

def cleanup_database():
    """Clean up all data from the SQLite database"""
    print("🗑️  Cleaning up database...")
    
    db_path = "instance/performance_analyzer.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables in database")
        
        # Delete data from all tables (in correct order to handle foreign keys)
        tables_to_clean = [
            'performance_records',
            'assessments', 
            'subjects',
            'students',
            'users'
        ]
        
        for table_name in tables_to_clean:
            try:
                cursor.execute(f"DELETE FROM {table_name}")
                deleted_count = cursor.rowcount
                print(f"   ✅ Deleted {deleted_count} records from {table_name}")
            except sqlite3.Error as e:
                print(f"   ⚠️  Could not clean {table_name}: {e}")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence")
        print("   ✅ Reset auto-increment counters")
        
        conn.commit()
        conn.close()
        
        print("✅ Database cleanup completed successfully")
        
    except Exception as e:
        print(f"❌ Database cleanup failed: {e}")

def cleanup_sample_files():
    """Remove all CSV and Excel files from sample_data directory"""
    print("\n🗑️  Cleaning up sample data files...")
    
    sample_data_dir = "sample_data"
    
    if not os.path.exists(sample_data_dir):
        print("❌ sample_data directory not found")
        return
    
    # File patterns to remove
    patterns = [
        "*.csv",
        "*.xlsx", 
        "*.xls",
        "*.CSV",
        "*.XLSX",
        "*.XLS"
    ]
    
    total_deleted = 0
    
    for pattern in patterns:
        files = glob.glob(os.path.join(sample_data_dir, pattern))
        for file_path in files:
            try:
                os.remove(file_path)
                print(f"   ✅ Deleted: {os.path.basename(file_path)}")
                total_deleted += 1
            except Exception as e:
                print(f"   ❌ Could not delete {file_path}: {e}")
    
    print(f"✅ Deleted {total_deleted} data files")

def cleanup_root_sample_files():
    """Remove sample files from root directory"""
    print("\n🗑️  Cleaning up root sample files...")
    
    # File patterns to remove from root
    patterns = [
        "sample_data/*.csv",
        "sample_data/*.xlsx", 
        "sample_data/*.xls",
        "*.csv",
        "*.xlsx",
        "*.xls"
    ]
    
    total_deleted = 0
    
    for pattern in patterns:
        files = glob.glob(pattern)
        for file_path in files:
            try:
                os.remove(file_path)
                print(f"   ✅ Deleted: {file_path}")
                total_deleted += 1
            except Exception as e:
                print(f"   ❌ Could not delete {file_path}: {e}")
    
    if total_deleted == 0:
        print("   ℹ️  No additional files found to delete")
    else:
        print(f"✅ Deleted {total_deleted} additional files")

def verify_cleanup():
    """Verify that cleanup was successful"""
    print("\n🔍 Verifying cleanup...")
    
    # Check database
    db_path = "instance/performance_analyzer.db"
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            tables_to_check = ['students', 'subjects', 'assessments', 'performance_records']
            
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    if count == 0:
                        print(f"   ✅ {table}: 0 records")
                    else:
                        print(f"   ⚠️  {table}: {count} records remaining")
                except sqlite3.Error:
                    print(f"   ❓ {table}: Table may not exist")
            
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Could not verify database: {e}")
    
    # Check files
    sample_data_dir = "sample_data"
    if os.path.exists(sample_data_dir):
        files = glob.glob(os.path.join(sample_data_dir, "*.*"))
        data_files = [f for f in files if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
        
        if len(data_files) == 0:
            print("   ✅ sample_data directory: No data files remaining")
        else:
            print(f"   ⚠️  sample_data directory: {len(data_files)} files remaining")
            for file in data_files:
                print(f"      - {os.path.basename(file)}")

def main():
    print("🧹 COMPREHENSIVE DATABASE AND FILE CLEANUP")
    print("=" * 60)
    print("This will:")
    print("  • Delete ALL data from the database")
    print("  • Remove ALL CSV/Excel files")
    print("  • Reset the system to a clean state")
    print("=" * 60)
    
    # Perform cleanup operations
    cleanup_database()
    cleanup_sample_files()
    cleanup_root_sample_files()
    verify_cleanup()
    
    print("\n" + "=" * 60)
    print("🎉 CLEANUP COMPLETED!")
    print("=" * 60)
    print("✅ Database is now empty and ready for new data")
    print("✅ All sample data files have been removed")
    print("✅ System is reset to clean state")
    print("\n💡 You can now upload your new 4th year CSE A datasets!")

if __name__ == "__main__":
    main()