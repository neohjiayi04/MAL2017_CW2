import pyodbc

try:
    # Connect to master database first
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=master;'
        'UID=SA;'
        'PWD=C0mp2001!;'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create the CW2 database
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'CW2') CREATE DATABASE CW2")
    print("✓ Database 'CW2' created successfully!")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
