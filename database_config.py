import pyodbc

# Database connection settings
connection_string = """
DRIVER={SQL Server};
SERVER=DESKTOP-RCFGB52;
DATABASE=EmployeeManagement;
"""

def get_db_connection():
    """Establish and return a database connection."""
    return pyodbc.connect(connection_string)
