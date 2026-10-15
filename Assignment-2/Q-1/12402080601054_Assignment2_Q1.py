```python
"""
Question 1: Regex-Based Email Intelligence Extractor

Description:
Extract valid email addresses ending in .com, .edu, or .org
from a text file. Display the unique email count and the
lexicographically smallest email for each domain.

Python Version: 3.10 or above
External Packages: None
"""

import re
import os


# Username may contain letters, digits, +, ., _, and -
# The domain contains one or more labels separated by dots.
# Only .com, .edu, and .org top-level domains are accepted.
EMAIL_PATTERN = re.compile(
    r'(?<![A-Za-z0-9+._-])'
    r'[A-Za-z0-9+._-]+'
    r'@'
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+'
    r'(?:com|edu|org)'
    r'(?![A-Za-z0-9.-])',
    re.IGNORECASE
)


def extract_emails(file_path):
    """Read the file line by line and collect unique valid emails."""
    unique_emails = set()

    # Use streaming so the entire file is not loaded into memory.
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            # Find all matching email addresses in the current line.
            matches = EMAIL_PATTERN.findall(line)

            for email in matches:
                # Normalize case so differently capitalized versions
                # of the same email are counted only once.
                unique_emails.add(email.lower())

    return unique_emails


def display_domain_summary(unique_emails):
    """Print each domain's count and smallest email."""
    domain_emails = {}

    # Group emails according to their complete domain.
    for email in unique_emails:
        domain = email.rsplit("@", 1)[1]
        domain_emails.setdefault(domain, []).append(email)

    # Print domains in lexicographic order.
    for domain in sorted(domain_emails):
        emails = domain_emails[domain]

        # Find the lexicographically smallest email.
        smallest_email = min(emails)

        print(domain, len(emails), smallest_email)


def main():
    """Validate the file path and execute the extractor."""
    file_path = input("Enter the text file path: ").strip()

    if not file_path:
        print("Error: File path cannot be empty.")
        return

    if not os.path.isfile(file_path):
        print("Error: The specified file does not exist.")
        return

    if not os.access(file_path, os.R_OK):
        print("Error: The file is not readable.")
        return

    try:
        unique_emails = extract_emails(file_path)

        if not unique_emails:
            print("No valid email addresses found.")
            return

        display_domain_summary(unique_emails)

    except (OSError, UnicodeError) as error:
        print(f"Error reading file: {error}")


if __name__ == "__main__":
    main()
```
