
# Assignment 2 - Q5: Tkinter Contact Manager with MySQL Backend

## 1. Problem Statement

Develop a Python GUI-based Contact Manager using Tkinter and MySQL.

The application allows users to create, update, delete, search and
display contacts. Contact details are stored persistently in a MySQL
database.

The application validates email addresses using regular expressions
and rejects duplicate email addresses.

The Contact table stores:

- Contact ID
- Name
- Email
- Phone
- Category
- Notes

## 2. Technologies Used

- Python 3.10 or above
- Tkinter
- MySQL
- mysql-connector-python
- Regular expressions (re)
- Entry and Text widgets
- Radio Button
- Listbox
- Menu
- Combobox
- Exception handling
- SQL CRUD operations

## 3. Requirements

- Python 3.10 or above
- MySQL Server
- mysql-connector-python package
- Visual Studio Code or another Python editor (recommended)

Install the MySQL connector using:

```bash
python -m pip install mysql-connector-python
```

Tkinter is included with most standard Windows Python installations.

## 4. Features

- Adds new contacts to the database.
- Displays saved contacts in a Listbox.
- Updates the selected contact.
- Deletes contacts after confirmation.
- Searches contacts by name, email or phone.
- Sorts contacts by name, email or category.
- Uses Entry widgets for name, email and phone.
- Uses a Text widget for notes.
- Uses radio buttons to select the search field.
- Uses a Combobox to select a contact category.
- Uses a Menu for refresh and exit operations.
- Validates email addresses using regex.
- Rejects duplicate emails.
- Uses a database UNIQUE constraint for email.
- Uses parameterized SQL statements for CRUD operations.
- Creates database tables and indexes automatically.
- Handles database connection and query errors.
- Supports persistent storage of large contact collections.

## 5. How to Run

### Step 1: Install Python

Install Python 3.10 or above.

Verify the installation:

```bash
python --version
```

### Step 2: Install the MySQL Connector

Run:

```bash
python -m pip install mysql-connector-python
```

### Step 3: Start MySQL Server

Ensure the MySQL Server service is running.

The default connection configuration uses localhost and port 3306.

### Step 4: Configure Database Credentials

Open the Python file and update DB_CONFIG with the correct
MySQL username and password.

### Step 5: Run the Program

Execute:

```bash
python 12402080601054_Assignment2_Q5.py
```

The application creates the contact_manager database and Contact
table automatically when the MySQL connection succeeds.

## 6. Input Format

The application accepts contact information through its GUI.

Fields:

- Name: Contact name
- Email: Contact email address
- Phone: Contact phone number
- Category: Personal, Faculty, Friend, Family or Work
- Notes: Additional information about the contact

Available operations:

- Add Contact
- Update Contact
- Delete Contact
- Clear Fields
- Search
- Show All
- Sort

Search can be performed by name, email or phone.

Email addresses must end in .com, .edu or .org according to the
regular expression used in this implementation.

Duplicate email addresses are rejected.

## 7. Output Format

The application displays an interactive contact list.

Example contact:

```text
ID | Name | Email | Phone | Category
1  | Asha | asha@adit.edu | 9876543210 | Faculty
```

After inserting a valid contact, the application displays the
contact in the list and updates the status message.

Invalid emails produce a validation warning. Duplicate emails
produce a duplicate-email error message.

## 8. Algorithm

1. Configure the MySQL connection settings.
2. Connect to MySQL Server.
3. Create the contact_manager database if it does not exist.
4. Create the Contact table and required indexes.
5. Initialize the Tkinter window and GUI widgets.
6. Accept contact details through the GUI.
7. Validate required fields and the email format.
8. For insertion, execute a parameterized INSERT statement.
9. For updating, execute a parameterized UPDATE statement.
10. For deletion, ask for confirmation and execute DELETE.
11. For searching, validate the selected search field and
    execute a parameterized SELECT query.
12. For sorting, use an allowed database column.
13. Display the retrieved records in the Listbox.
14. Handle duplicate emails and database errors.
15. Refresh the contact list after successful operations.

## 9. Time and Space Complexity

Let N be the total number of contacts and R be the number of
matching contacts returned by a search.

- Indexed exact-match search: Typically O(log N) to locate
  matching entries, plus the cost of returning results.
- Indexed prefix search: Can use a suitable index, depending
  on the database query plan and collation.
- Unindexed search: O(N) in the worst case.
- Sorting: May require O(N log N) when the database cannot
  satisfy the requested ordering using an index.
- Insert, update and delete: Depend on indexes and the database
  execution plan.
- Python result storage: O(R) for the contacts returned.

The application creates indexes on name and phone. The UNIQUE
constraint on email also creates an index. Actual performance
depends on the data distribution and query plan.

## 10. Test Cases

### Test 1: Add a Valid Contact

Input:

- Name: Asha
- Email: asha@adit.edu
- Phone: 9876543210
- Category: Faculty
- Notes: Python instructor

Expected result:

- Contact inserted successfully.
- Asha appears in the contact list.

### Test 2: Invalid Email

Input:

- Name: Riya
- Email: riya@invalid.xyz
- Phone: 9876543211
- Category: Personal

Expected result:

- Invalid Email warning is displayed.
- The contact is not inserted.

### Test 3: Duplicate Email

First contact:

- Name: Asha
- Email: asha@adit.edu

Second contact:

- Name: Meera
- Email: asha@adit.edu

Expected result:

- Duplicate Email error is displayed.
- The second contact is rejected.

### Additional Tests

- Update an existing contact.
- Delete a selected contact.
- Search by name.
- Search by email.
- Search by phone.
- Sort contacts by email or category.
- Restart the application and verify persistence.

## 11. Limitations

- A running MySQL Server is required.
- Database credentials must be configured correctly.
- The email validation pattern accepts only .com, .edu
  and .org addresses.
- Search uses prefix matching rather than arbitrary substring
  matching.
- Search and sorting performance depends on database indexes
  and the query execution plan.
- The GUI displays the contacts returned by the current query.
- Large result sets may take time to display and sort.
