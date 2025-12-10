import pyodbc

# Try different server names
servers = [
    'localhost',
    '(local)',
    '.',
    'localhost\\SQLEXPRESS',
    '.\\SQLEXPRESS',
    '(localdb)\\MSSQLLocalDB'
]

for server in servers:
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};'
            f'SERVER={server};'
            f'DATABASE=master;'  # Try connecting to master database first
            f'UID=SA;'
            f'PWD=C0mp2001!;'
        )
        print(f"✓ Connection successful with SERVER={server}")
        conn.close()
        break
    except Exception as e:
        print(f"✗ Failed with SERVER={server}")