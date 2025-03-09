from flask import Flask, request, render_template, redirect
from database_config import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Employee routes
@app.route('/employees', methods=['GET'])
def view_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template('view_employees.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Employees (Name, Email, Phone, Department) 
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, department))
        conn.commit()
        conn.close()
        return redirect('/employees')

    return render_template('add_employee.html')

@app.route('/update_employee/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        cursor.execute("""
            UPDATE Employees
            SET Name = ?, Email = ?, Phone = ?, Department = ?
            WHERE EmployeeID = ?
        """, (name, email, phone, department, id))
        conn.commit()
        conn.close()
        return redirect('/employees')

    cursor.execute("SELECT * FROM Employees WHERE EmployeeID = ?", (id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('update_employee.html', employee=employee)

@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, delete related entries in EmployeeProjects
    cursor.execute("DELETE FROM EmployeeProjects WHERE EmployeeID = ?", (id,))

    # Then, delete the employee
    cursor.execute("DELETE FROM Employees WHERE EmployeeID = ?", (id,))
    
    conn.commit()
    conn.close()
    return redirect('/employees')


# Project routes
@app.route('/projects', methods=['GET'])
def view_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projects")
    projects = cursor.fetchall()
    conn.close()
    return render_template('view_projects.html', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        project_name = request.form['project_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = request.form['budget']
        employee_id = request.form['employee_id']  # Employee ID from form

        # Insert into Projects table & get the inserted ProjectID
        cursor.execute("""
            INSERT INTO Projects (ProjectName, StartDate, EndDate, Budget) 
            OUTPUT INSERTED.ProjectID
            VALUES (?, ?, ?, ?);
        """, (project_name, start_date, end_date, budget))
        
        project_id = cursor.fetchone()[0]  # Get ProjectID

        # Insert into EmployeeProjects table
        cursor.execute("""
            INSERT INTO EmployeeProjects (EmployeeID, ProjectID) 
            VALUES (?, ?);
        """, (employee_id, project_id))

        conn.commit()
        conn.close()
        return redirect('/projects')

    # Fetch employees for dropdown
    cursor.execute("SELECT EmployeeID, Name FROM Employees")
    employees = cursor.fetchall()
    conn.close()

    return render_template('add_project.html', employees=employees)


@app.route('/update_project/<int:id>', methods=['GET', 'POST'])
def update_project(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        project_name = request.form['project_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = request.form['budget']
        cursor.execute("""
            UPDATE Projects
            SET ProjectName = ?, StartDate = ?, EndDate = ?, Budget = ?
            WHERE ProjectID = ?
        """, (project_name, start_date, end_date, budget, id))
        conn.commit()
        conn.close()
        return redirect('/projects')

    cursor.execute("SELECT * FROM Projects WHERE ProjectID = ?", (id,))
    project = cursor.fetchone()
    conn.close()
    return render_template('update_project.html', project=project)

@app.route('/delete_project/<int:id>', methods=['GET', 'POST'])
def delete_project(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, delete related entries in EmployeeProjects
    cursor.execute("DELETE FROM EmployeeProjects WHERE ProjectID = ?", (id,))

    # Then, delete the project
    cursor.execute("DELETE FROM Projects WHERE ProjectID = ?", (id,))

    conn.commit()
    conn.close()
    return redirect('/projects')

@app.route('/employee_projects', methods=['GET'])
def view_employee_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ep.EmployeeID, e.Name, ep.ProjectID, p.ProjectName 
        FROM EmployeeProjects ep
        JOIN Employees e ON ep.EmployeeID = e.EmployeeID
        JOIN Projects p ON ep.ProjectID = p.ProjectID
    """)
    employee_projects = cursor.fetchall()
    conn.close()
    return render_template('view_employee_projects.html', employee_projects=employee_projects)



if __name__ == '__main__':
    app.run(debug=True)
