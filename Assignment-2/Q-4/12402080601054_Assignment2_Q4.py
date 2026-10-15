import re
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "query_builder.db"

# Only these fields can be used in queries.
COLUMNS = {
    "student.id": "s.student_id",
    "student.student_id": "s.student_id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.course_id",
    "course.course_id": "c.course_id",
    "course.name": "c.name",
    "registration.student_id": "r.student_id",
    "registration.course_id": "r.course_id",
}

FILTER_OPERATORS = ["LIKE", ">=", "<=", "!=", "=", ">", "<"]


def setup_database(connection):
    """Create tables and insert sample data."""
    connection.execute("PRAGMA foreign_keys = ON")

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            spi REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Course (
            course_id TEXT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INTEGER NOT NULL,
            course_id TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Student(student_id),
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
        );
    """)

    students = [
        (2201, "Asha", 9.1),
        (2207, "Dev", 8.4),
        (2208, "Riya", 7.5),
        (2210, "Meera", 8.0),
    ]

    courses = [
        ("PY101", "Programming with Python"),
        ("DB101", "Database Management"),
    ]

    registrations = [
        (2201, "PY101"),
        (2207, "PY101"),
        (2208, "PY101"),
        (2210, "PY101"),
        (2201, "DB101"),
        (2208, "DB101"),
    ]

    connection.executemany(
        "INSERT OR IGNORE INTO Student VALUES (?, ?, ?)", students
    )
    connection.executemany(
        "INSERT OR IGNORE INTO Course VALUES (?, ?)", courses
    )
    connection.executemany(
        "INSERT OR IGNORE INTO CourseRegistration VALUES (?, ?)",
        registrations,
    )


def parse_filter(condition):
    """Validate a filter and return its SQL and parameter."""
    condition = condition.strip()

    for operator in FILTER_OPERATORS:
        if operator in condition:
            column, value = condition.split(operator, 1)
            column = column.strip().lower()
            value = value.strip()

            if column not in COLUMNS:
                raise ValueError(f"Invalid filter column: {column}")

            if not value:
                raise ValueError("Filter value cannot be empty.")

            # Values are always passed as parameters, never SQL text.
            return f"{COLUMNS[column]} {operator} ?", value

    raise ValueError(
        "Invalid filter. Use =, !=, >, <, >=, <= or LIKE."
    )


def build_query(columns, filters, order_column, direction, limit):
    """Validate the request and build a parameterized SQL query."""

    if not columns:
        raise ValueError("Select at least one column.")

    selected_columns = []
    for column in columns:
        column = column.strip().lower()

        if column not in COLUMNS:
            raise ValueError(f"Invalid selected column: {column}")

        selected_columns.append(COLUMNS[column])

    order_column = order_column.strip().lower()
    if order_column not in COLUMNS:
        raise ValueError(f"Invalid order column: {order_column}")

    direction = direction.strip().upper()
    if direction not in ("ASC", "DESC"):
        raise ValueError("Sort direction must be ASC or DESC.")

    if not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError("LIMIT must be between 1 and 1000.")

    where_parts = []
    parameters = []

    for condition in filters:
        sql_part, value = parse_filter(condition)
        where_parts.append(sql_part)
        parameters.append(value)

    sql = (
        "SELECT " + ", ".join(selected_columns) +
        " FROM Student AS s "
        "JOIN CourseRegistration AS r ON s.student_id = r.student_id "
        "JOIN Course AS c ON r.course_id = c.course_id"
    )

    if where_parts:
        sql += " WHERE " + " AND ".join(where_parts)

    sql += f" ORDER BY {COLUMNS[order_column]} {direction} LIMIT ?"
    parameters.append(limit)

    return sql, parameters


def main():
    try:
        print("SQL Join Query Builder and Validator")
        print("------------------------------------")
        print("Available columns:")
        print(", ".join(COLUMNS.keys()))
        print("\nUse commas to separate multiple columns or filters.")
        print("Example filter: course.id=PY101")

        columns = input("\nSelected columns: ").split(",")
        filter_text = input("WHERE filters (blank for none): ").strip()
        filters = [item.strip() for item in filter_text.split(",")
                   if item.strip()]

        order_column = input("Order column: ")
        direction = input("Sort direction (ASC/DESC): ")
        limit = int(input("LIMIT (1-1000): "))

        sql, parameters = build_query(
            columns, filters, order_column, direction, limit
        )

        with sqlite3.connect(DB_FILE) as connection:
            setup_database(connection)
            results = connection.execute(sql, parameters).fetchall()

        print("\nSQL_OK")
        print("\nGenerated SQL template:")
        print(sql)
        print("\nParameters:")
        print(parameters)
        print("\nQuery results:")

        if not results:
            print("No matching records found.")
        else:
            print(" | ".join(c.strip() for c in columns))
            for row in results:
                print(" | ".join(str(value) for value in row))

    except ValueError as error:
        print("\nVALIDATION_ERROR:", error)
    except sqlite3.Error as error:
        print("\nDATABASE_ERROR:", error)


if __name__ == "__main__":
    main()
