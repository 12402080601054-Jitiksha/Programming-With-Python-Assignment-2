
import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE_FILE = BASE_DIR / "student_analytics.db"
STUDENTS_FILE = BASE_DIR / "students.csv"
REGISTRATIONS_FILE = BASE_DIR / "registrations.csv"


def create_tables(connection):
    """Create the required database tables."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            spi REAL NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INTEGER NOT NULL,
            course_id TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
        )
    """)


def import_students(connection):
    """Import student records from CSV."""
    with open(STUDENTS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = int(row["student_id"])
            name = row["name"].strip()
            spi = float(row["spi"])

            if not name or not 0 <= spi <= 10:
                raise ValueError("Invalid student name or SPI.")

            connection.execute("""
                INSERT INTO Student (student_id, name, spi)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    name = excluded.name,
                    spi = excluded.spi
            """, (student_id, name, spi))


def import_registrations(connection):
    """Import course registrations from CSV."""
    with open(REGISTRATIONS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = int(row["student_id"])
            course_id = row["course_id"].strip()

            if not course_id:
                raise ValueError("Course ID cannot be empty.")

            connection.execute("""
                INSERT OR IGNORE INTO CourseRegistration
                (student_id, course_id)
                VALUES (?, ?)
            """, (student_id, course_id))


def find_students(connection, course_id, threshold):
    """Find eligible students in the selected course."""
    cursor = connection.execute("""
        SELECT s.student_id, s.name, s.spi
        FROM Student AS s
        INNER JOIN CourseRegistration AS r
            ON s.student_id = r.student_id
        WHERE r.course_id = ? AND s.spi > ?
        ORDER BY s.spi DESC, s.student_id ASC
    """, (course_id, threshold))

    return cursor.fetchall()


def main():
    try:
        course_id = input("Enter course ID: ").strip()
        threshold_text = input("Enter minimum SPI threshold: ").strip()

        if not course_id:
            raise ValueError("Course ID cannot be empty.")

        threshold = float(threshold_text)

        if not 0 <= threshold <= 10:
            raise ValueError("SPI threshold must be between 0 and 10.")

        with sqlite3.connect(DATABASE_FILE) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            create_tables(connection)
            import_students(connection)
            import_registrations(connection)

            results = find_students(connection, course_id, threshold)

            print("\nEligible Students")
            print("-" * 45)

            if not results:
                print("No matching students found.")
            else:
                print(f"{'Student ID':<15}{'Name':<15}{'SPI':>8}")
                for student_id, name, spi in results:
                    print(f"{student_id:<15}{name:<15}{spi:>8.2f}")

    except ValueError as error:
        print("Input or data error:", error)
    except (sqlite3.Error, OSError, csv.Error, KeyError) as error:
        print("Database or file error:", error)


if __name__ == "__main__":
    main()
