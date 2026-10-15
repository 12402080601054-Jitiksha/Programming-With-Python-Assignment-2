
# Assignment 2 - Q1: Regex-Based Email Intelligence Extractor

## 1. Problem Statement

Develop a Python program that reads a text file and extracts valid email
addresses ending in `.com`, `.edu`, or `.org`.

The program ignores malformed email addresses and counts unique email
addresses. For each complete email domain, it displays:

- Domain name
- Number of unique email addresses
- Lexicographically smallest email address

## 2. Technologies Used

- Python 3.10 or above
- Regular expressions (`re`)
- Sets and dictionaries
- File handling
- Command-line arguments (`sys`)
- Path validation (`pathlib`)

## 3. Requirements

- Python 3.10 or above
- No external packages required


## 4. Features

- Extracts email addresses using regular expressions.
- Accepts `.com`, `.edu`, and `.org` top-level domains.
- Ignores malformed email addresses.
- Removes duplicate email addresses using a set.
- Processes files line by line.
- Displays domains in lexicographical order.
- Displays the number of unique emails for each domain.
- Finds the lexicographically smallest email for each domain.
- Handles invalid paths, missing files, and file-access errors.
- Normalizes email addresses to lowercase.

## 5. How to Run

### Step 1: Install Python

Install Python 3.10 or above.

Verify the installation:

```bash
python --version
```

### Step 2: Open the Project Folder

Open a terminal or command prompt in the project folder.

### Step 3: Run the Program

Replace `YOUR_ENROLLMENT_NO` with your actual enrollment number.

```bash
python YOUR_ENROLLMENT_NO_Assignment2_Q1.py sample.txt
```

### Step 4: Use Another Text File

```bash
python YOUR_ENROLLMENT_NO_Assignment2_Q1.py input.txt
```

Replace `input.txt` with the path to your text file.

## 6. Input Format

The program accepts the path of a text file as a command-line argument.

The file can contain ordinary text, valid email addresses, duplicate
email addresses, and malformed email addresses.

## 7. Output Format

For every domain, the program displays:

```text
domain unique_email_count smallest_email
```

Domains are displayed in lexicographical order.

## 8. Algorithm

1. Accept the input file path.
2. Validate the path.
3. Open the file in read mode.
4. Read the file one line at a time.
5. Apply the regular expression to identify candidate email addresses.
6. Ignore addresses that do not match the accepted format.
7. Convert accepted email addresses to lowercase.
8. Store unique email addresses in a set.
9. Group the unique addresses by their complete domain.
10. Sort the domains lexicographically.
11. Calculate the number of unique addresses for each domain.
12. Find the lexicographically smallest address in each domain.
13. Display the results.

## 9. Time and Space Complexity

Let N be the total number of characters in the input file and U be
the number of unique email addresses extracted.

- Expected extraction time: O(N)
- Expected storage space: O(U)
- Additional sorting time: Depends on the number of unique domains
  and the number of emails processed for minimum selection.

The implementation processes the file line by line rather than
loading the entire file into memory.

## 10. Test Cases

Test 1: Duplicate email

Input:
`user@example.com user@example.com`

Expected result:
The domain `example.com` has one unique email.

Test 2: Multiple domains

Input:
`a@site.com b@site.org c@site.edu`

Expected result:
Three domains are displayed in lexicographical order, each with
one unique email.

Test 3: Malformed email addresses

Input:
`root@@bad.com @missing.com user@domain.xyz`

Expected result:
No email addresses are extracted.

Test 4: Multiple emails with the same domain

Input:
`z@sample.org a@sample.org m@sample.org`

Expected result:
The domain `sample.org` has three unique emails, and `a@sample.org`
is the lexicographically smallest email.

Test 5: Empty file

Input:
An empty text file.

Expected result:
No domain summaries are displayed.

Test 6: Invalid file path

Input:
A path that does not point to an existing file.

Expected result:
An appropriate error message is displayed.

## 11. Limitations

- The extractor follows the email format specified in this assignment
  and is not a complete implementation of every email-address standard.
- Email addresses are treated as case-insensitive for deduplication.
- The set stores all unique email addresses, so memory usage increases
  with the number of unique addresses.

