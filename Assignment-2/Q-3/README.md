# Student-Course Analytics Engine

## Description

This project analyzes student-course registration data using Python and SQLite.

It reads student information from students.csv and course
registrations from registrations.csv. It creates the required
database tables and finds students registered for a specified
course whose SPI is greater than a given threshold.

The results are sorted by SPI in descending order and student ID
in ascending order.

## Features

- Imports student records from CSV.
- Imports course registration records from CSV.
- Creates Student and CourseRegistration tables.
- Uses parameterized SQL queries.
- Handles invalid inputs and database/file errors.
- Sorts eligible students according to the required conditions.
- Uses SQLite, which is included with Python.

## Files

- 12402080601054_Assignment2_Q3.py: Main Python program
- students.csv: Student details
- registrations.csv: Course registration details
- README.md: Project documentation

The student_analytics.db file is created automatically when the
program runs.

## Requirements

- Python 3.10 or later
- Visual Studio Code (recommended)

No external Python packages or MySQL installation are required.

## How to Run

1. Open the project folder in VS Code.
2. Open the integrated terminal.
3. Run the following command:

   python 12402080601054_Assignment2_Q3.py

4. Enter the course ID.
5. Enter the minimum SPI threshold.
6. View the eligible students.

## Test Cases

### Test Case 1

Input:
- Course ID: PY101
- SPI threshold: 8.0

Expected result:
- 2201, Asha, 9.10
- 2207, Dev, 8.40
- 2212, Kabir, 8.40

### Test Case 2

Input:
- Course ID: DB101
- SPI threshold: 7.0

Expected result:
- 2201, Asha, 9.10
- 2210, Meera, 8.00
- 2208, Riya, 7.50

### Test Case 3

Input:
- Course ID: PY101
- SPI threshold: 9.5

Expected result:
- No matching students found.

## Exception Handling

The program handles invalid input, invalid CSV data, missing
files, and SQLite errors using exception handling.

## Note

This implementation uses SQLite instead of MySQL. If MySQL is
mandatory for the assignment, confirm whether SQLite is accepted.
