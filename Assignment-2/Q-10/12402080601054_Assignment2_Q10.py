
"""
Q10: Python Data Visualization Dashboard Exporter
Reads student marks from CSV, cleans missing values, calculates
subject statistics, and exports three charts.
Python 3.10+
"""

import os
import sys
import pandas as pd
import matplotlib

# Use a non-interactive backend so charts save without opening windows.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


IDENTITY_COLUMNS = ["enrollment", "name"]
MAX_STUDENTS = 1_000_000
MAX_SUBJECTS = 20

GRADE_LABELS = ["A (90-100)", "B (80-89)", "C (70-79)",
                "D (60-69)", "F (below 60)"]


def read_marks(csv_path):
    """Read the CSV and validate its structure and marks."""
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    df = pd.read_csv(csv_path, dtype={"enrollment": "string",
                                      "name": "string"})

    if df.empty:
        raise ValueError("The CSV contains no student records.")

    if not all(col in df.columns for col in IDENTITY_COLUMNS):
        raise ValueError("CSV must contain enrollment and name columns.")

    if df.columns.duplicated().any():
        raise ValueError("CSV contains duplicate column names.")

    subject_columns = [
        col for col in df.columns if col not in IDENTITY_COLUMNS
    ]

    if not subject_columns:
        raise ValueError("At least one subject column is required.")

    if len(subject_columns) > MAX_SUBJECTS:
        raise ValueError(f"Maximum allowed subjects: {MAX_SUBJECTS}.")

    if len(df) > MAX_STUDENTS:
        raise ValueError(f"Maximum allowed students: {MAX_STUDENTS}.")

    if df[IDENTITY_COLUMNS].isna().any().any():
        raise ValueError("Enrollment and name cannot be missing.")

    if df[IDENTITY_COLUMNS].apply(
        lambda col: col.str.strip().eq("").any()
    ).any():
        raise ValueError("Enrollment and name cannot be blank.")

    # Convert marks to numeric. Non-numeric or out-of-range marks
    # are treated as missing and filled during the cleaning step.
    for subject in subject_columns:
        values = pd.to_numeric(df[subject], errors="coerce")
        values = values.where(values.between(0, 100))
        df[subject] = values

    return df, subject_columns


def clean_marks(df, subjects):
    """Replace missing or invalid marks with each subject's mean."""
    cleaned = df.copy()

    for subject in subjects:
        subject_mean = cleaned[subject].mean()

        # If every mark is missing, use 0 as a documented fallback.
        if pd.isna(subject_mean):
            subject_mean = 0

        cleaned[subject] = cleaned[subject].fillna(subject_mean)

    cleaned[subjects] = cleaned[subjects].round(2)
    return cleaned


def calculate_summary(cleaned, subjects):
    """Calculate subject-wise descriptive statistics."""
    summary_rows = []

    for subject in subjects:
        marks = cleaned[subject]

        summary_rows.append({
            "subject": subject,
            "students": len(marks),
            "average": round(marks.mean(), 2),
            "median": round(marks.median(), 2),
            "minimum": round(marks.min(), 2),
            "maximum": round(marks.max(), 2),
            "standard_deviation": round(marks.std(ddof=0), 2)
        })

    return pd.DataFrame(summary_rows)


def assign_grade(mark):
    """Assign a grade to an individual subject mark."""
    if mark >= 90:
        return GRADE_LABELS[0]
    if mark >= 80:
        return GRADE_LABELS[1]
    if mark >= 70:
        return GRADE_LABELS[2]
    if mark >= 60:
        return GRADE_LABELS[3]
    return GRADE_LABELS[4]


def export_grade_chart(cleaned, subjects, output_folder):
    """Export the distribution of grades across all subject marks."""
    all_marks = cleaned[subjects].to_numpy().ravel()
    grades = pd.Series(all_marks).map(assign_grade)
    counts = grades.value_counts().reindex(GRADE_LABELS, fill_value=0)

    plt.figure(figsize=(9, 5))
    counts.plot(kind="bar", edgecolor="black")
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Marks")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "grade_distribution.png"),
                dpi=150)
    plt.close()


def export_subject_chart(summary, output_folder):
    """Export a bar chart comparing subject averages."""
    plt.figure(figsize=(9, 5))
    plt.bar(summary["subject"], summary["average"], edgecolor="black")
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "subject_average.png"),
                dpi=150)
    plt.close()


def export_top_performers(cleaned, subjects, output_folder):
    """Export the top 10 students by average marks."""
    result = cleaned[IDENTITY_COLUMNS].copy()
    result["average_marks"] = cleaned[subjects].mean(axis=1).round(2)

    # Stable sorting makes ties predictable.
    result = result.sort_values(
        ["average_marks", "enrollment"],
        ascending=[False, True],
        kind="stable"
    ).head(10)

    plt.figure(figsize=(10, 5))
    labels = result["name"].astype(str) + " (" + \
        result["enrollment"].astype(str) + ")"

    plt.barh(labels.iloc[::-1], result["average_marks"].iloc[::-1],
             edgecolor="black")
    plt.title("Top 10 Student Performers")
    plt.xlabel("Average Marks")
    plt.ylabel("Student")
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "top_performers.png"),
                dpi=150)
    plt.close()


def main():
    """Run the complete data-cleaning and visualization pipeline."""
    try:
        csv_path = input("Enter path of marks CSV file: ").strip()
        output_folder = input("Enter output folder path: ").strip()

        if not csv_path or not output_folder:
            raise ValueError("Input file path and output folder are required.")

        df, subjects = read_marks(csv_path)
        cleaned = clean_marks(df, subjects)
        summary = calculate_summary(cleaned, subjects)

        os.makedirs(output_folder, exist_ok=True)

        cleaned_path = os.path.join(output_folder, "cleaned_marks.csv")
        summary_path = os.path.join(output_folder, "summary.csv")

        cleaned.to_csv(cleaned_path, index=False)
        summary.to_csv(summary_path, index=False)

        export_grade_chart(cleaned, subjects, output_folder)
        export_subject_chart(summary, output_folder)
        export_top_performers(cleaned, subjects, output_folder)

        print("\nDashboard export completed successfully.")
        print(f"Cleaned CSV: {cleaned_path}")
        print(f"Summary CSV: {summary_path}")
        print(f"Charts saved in: {os.path.abspath(output_folder)}")
        print("\nSubject-wise summary:")
        print(summary.to_string(index=False))

    except (OSError, ValueError, pd.errors.ParserError,
            pd.errors.EmptyDataError) as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
