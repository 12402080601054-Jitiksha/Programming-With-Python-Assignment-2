
# Assignment 2 - Q4: SQL Join Query Builder and Validator

## 1. Problem Statement

Develop a Python program that builds and validates SQL queries for
joining Student, Course and CourseRegistration tables.

The program accepts selected columns, filter conditions, sorting
options and a result limit. It generates a safe parameterized SQL
query, validates user input and displays the query results.

The program supports:

- Selected projection fields
- WHERE conditions
- Equality, range and LIKE filters
- ORDER BY with ASC or DESC
- LIMIT between 1 and 1000
- SQL injection prevention using parameterized queries
- Validation of table and column names

## 2. Technologies Used

- Python 3.10 or above
- SQLite database
- SQL joins
- Parameterized SQL queries
- Dictionaries
- Lists and string handling
- Exception handling
- Input validation

## 3. Requirements

- Python 3.10 or above
- Visual Studio Code or another Python editor (recommended)
- No external Python packages required
- No MySQL installation required

## 4. Features

- Creates Student, Course and CourseRegistration tables.
- Joins the three tables using their related identifiers.
- Accepts selected projection fields.
- Supports multiple WHERE filter conditions.
- Supports equality (=) and inequality (!=) operators.
- Supports range operators (>, <, >= and <=).
- Supports LIKE filters.
- Supports ORDER BY with ASC or DESC.
- Validates LIMIT values between 1 and 1000.
- Allows only whitelisted column names.
- Rejects invalid columns and sort directions.
- Uses parameterized SQL to help prevent SQL injection.
- Displays the generated SQL template.
- Displays the SQL parameters separately.
- Displays the query result table.
- Handles validation and database errors.

## 5. How to Run

### Step 1: Install Python

Install Python 3.10 or above.

Verify the installation:

```bash
python --version
```

### Step 2: Open the Project Folder

Open the Q-4 project folder in Visual Studio Code.

Open the integrated terminal using:

Terminal -> New Terminal

### Step 3: Run the Program

Execute the following command:

```bash
python 12402080601054_Assignment2_Q4.py
```

### Step 4: Enter Query Details

Enter the selected columns, WHERE filters, order column,
sort direction and limit when prompted.

Example:

```text
Selected columns: student.name, course.name
WHERE filters (blank for none): course.id=PY101
Order column: student.spi
Sort direction (ASC/DESC): DESC
LIMIT (1-1000): 2
```

The program displays SQL_OK, the generated SQL template,
the parameter list and the query results.

## 6. Input Format

The program accepts the following inputs interactively:

1. Selected columns, separated by commas.
2. WHERE filter conditions, separated by commas.
3. Order column.
4. Sort direction: ASC or DESC.
5. LIMIT: an integer between 1 and 1000.

Example:

```text
Selected columns: student.name, course.name
WHERE filters (blank for none): course.id=PY101
Order column: student.spi
Sort direction (ASC/DESC): DESC
LIMIT (1-1000): 2
```

Available column names include:

- student.id
- student.student_id
- student.name
- student.spi
- course.id
- course.course_id
- course.name
- registration.student_id
- registration.course_id

Supported filter operators:

- =
- !=
- >
- <
- >=
- <=
- LIKE

Multiple filters are combined using AND.

## 7. Output Format

The program displays:

- Validation status
- Generated SQL template
- SQL parameter list
- Query results

Example:

```text
SQL_OK

Generated SQL template:
SELECT s.name, c.name FROM Student AS s JOIN CourseRegistration AS r ON s.student_id = r.student_id JOIN Course AS c ON r.course_id = c.course_id WHERE c.course_id = ? ORDER BY s.spi DESC LIMIT ?

Parameters:
['PY101', 2]

Query results:
student.name | course.name
Asha | Programming with Python
Dev | Programming with Python
```

## 8. Algorithm

1. Accept selected columns from the user.
2. Validate the selected columns against the whitelist.
3. Accept and validate the WHERE filter conditions.
4. Check that each filter uses a supported operator.
5. Accept and validate the order column.
6. Validate the sort direction as ASC or DESC.
7. Validate that LIMIT is between 1 and 1000.
8. Construct the SELECT statement using validated column names.
9. Add JOIN clauses to connect Student, CourseRegistration
   and Course tables.
10. Add WHERE conditions using parameter placeholders.
11. Add ORDER BY and LIMIT clauses.
12. Execute the query using parameterized SQL.
13. Display the generated SQL, parameters and results.
14. Handle invalid input and database errors.

## 9. Time and Space Complexity

Let F be the number of filter conditions, P be the number of
selected projection fields, and R be the number of returned rows.

- Query construction and validation: O(F + P)
- Result storage: O(R), where R is at most the specified limit
- Database execution: Depends on the query plan, table sizes
  and available indexes.

The program validates requested columns and filters before
executing the generated query.

## 10. Test Cases

### Test 1: Basic Join Query

Input:

```text
Selected columns: student.name, course.name
WHERE filters (blank for none): course.id=PY101
Order column: student.spi
Sort direction (ASC/DESC): DESC
LIMIT (1-1000): 2
```

Expected result:

```text
SQL_OK

Parameters:
['PY101', 2]

Query results:
student.name | course.name
Asha | Programming with Python
Dev | Programming with Python
```

### Test 2: Range and LIKE Filters

Input:

```text
Selected columns: student.name, student.spi
WHERE filters (blank for none): student.spi>=8.0, student.name LIKE A%
Order column: student.spi
Sort direction (ASC/DESC): DESC
LIMIT (1-1000): 10
```

Expected result:

```text
SQL_OK

Parameters:
['8.0', 'A%', 10]

Query results:
student.name | student.spi
Asha | 9.1
```

### Test 3: Invalid Column

Input:

```text
Selected columns: student.name, student.password
WHERE filters (blank for none):
Order column: student.spi
Sort direction (ASC/DESC): DESC
LIMIT (1-1000): 5
```

Expected result:

```text
VALIDATION_ERROR: Invalid selected column: student.password
```

The program rejects the invalid column before executing
the SQL query.

### Additional Validation Tests

- Invalid sort direction: Enter a value other than ASC or DESC.
- Invalid limit: Enter 0, a negative number or a value greater
  than 1000.
- Invalid filter column: Enter a column that is not whitelisted.
- SQL injection attempt: Enter SQL syntax as a filter value
  and verify that it is treated as a parameter.

## 11. Limitations

- The program uses SQLite rather than MySQL.
- Only predefined tables and whitelisted columns are supported.
- Multiple filter conditions are combined using AND.
- Complex nested conditions using OR and parentheses are not supported.
- The program supports only the listed filter operators.
- The database query execution time depends on the query plan
  and the size of the data.
- Parameterized queries protect filter values, while identifiers
  must be validated separately using the whitelist.
- The program uses sample student and course data for testing.
