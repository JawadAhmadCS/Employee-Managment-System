
--as ka jo project ha employee wala as ko run krna ka lia as ma values nhi dalni
--keo ka yha wali values web ma delete nhi hotin



-- Create the database
CREATE DATABASE EmployeeManagement;

-- Switch to the EmployeeManagement database
USE EmployeeManagement;

select @@SERVERNAME

SELECT @@SERVERNAME AS ServerName;

SELECT HOST_NAME() AS HostName;

-- Create the Employees table
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1), -- Auto-incremented ID
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(20) NOT NULL,
    Department VARCHAR(50) NOT NULL
);

-->start----------------------no run this to add values---------------------------
-- Add sample data into Employees table
INSERT INTO Employees (Name, Email, Phone, Department)
VALUES
('John Doe', 'john.doe@example.com', '123-456-7890', 'HR'),
('Jane Smith', 'jane.smith@example.com', '234-567-8901', 'Finance'),
('Sara Lee', 'sara.lee@example.com', '345-678-9012', 'IT'),
('Michael Brown', 'michael.brown@example.com', '456-789-0123', 'Sales');
------------------------yha tk nhi krna-------------------------end<--


-- Create the Projects table
CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY IDENTITY(1,1), -- Auto-incremented ID
    ProjectName VARCHAR(100) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Budget DECIMAL(10, 2)
);


-->start----------------------no run this to add values---------------------------
-- Add sample data into Projects table
INSERT INTO Projects (ProjectName, StartDate, EndDate, Budget)
VALUES
('Project A', '2025-01-01', '2025-12-31', 50000.00),
('Project B', '2025-02-01', NULL, 30000.00);
------------------------yha tk nhi krna-------------------------end<--


-- Create the EmployeeProjects table to represent the many-to-many relationship
CREATE TABLE EmployeeProjects (
    EmployeeID INT,
    ProjectID INT,
    PRIMARY KEY (EmployeeID, ProjectID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);


-->start----------------------no run this to add values---------------------------
-- Add sample data into EmployeeProjects table
INSERT INTO EmployeeProjects (EmployeeID, ProjectID)
VALUES
(1, 1),
(2, 2),
(3, 1),
(4, 2);
------------------------yha tk nhi krna-------------------------end<--

ALTER TABLE EmployeeProjects 
ADD CONSTRAINT FK_EmployeeProjects_EmployeeID 
FOREIGN KEY (EmployeeID) 
REFERENCES Employees(EmployeeID) 
ON DELETE CASCADE;

ALTER TABLE EmployeeProjects 
ADD CONSTRAINT FK_EmployeeProjects_ProjectID 
FOREIGN KEY (ProjectID) 
REFERENCES Projects(ProjectID) 
ON DELETE CASCADE;

-- SELECT * FROM Employees;

DELETE FROM Employees
WHERE EmployeeID = 1; -- Deletes the employee with EmployeeID = 1

DELETE FROM Employees
WHERE EmployeeID = 2; -- Deletes the employee with EmployeeID = 1

DELETE FROM Employees
WHERE EmployeeID = 3; -- Deletes the employee with EmployeeID = 1

DELETE FROM Employees
WHERE EmployeeID = 4; -- Deletes the employee with EmployeeID = 1

DELETE FROM Projects  
WHERE ProjectID = 1;