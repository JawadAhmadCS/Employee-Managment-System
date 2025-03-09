import pypyodbc as odbc

# Update these values to your settings
DRIVER_NAME = 'SQL Server'  # Make sure this driver is installed
SERVER_NAME = 'DESKTOP-RCFGB52'  # SQL Server address
DATABASE_NAME = 'EmployeeManagement'

# Connection string
connection_string = f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
"""

try:
    # Establish connection
    conn = odbc.connect(connection_string)
    print("Connection Successful!")

    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT DB_NAME();")
    current_db = cursor.fetchone()
    print(f"Connected to database: {current_db[0]}")

    # Example: Insert data (if `users` table exists)
    cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com')")
    conn.commit()
    print("Data inserted successfully.")

    # Fetch and display data
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except odbc.Error as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
        print("Connection closed.")
