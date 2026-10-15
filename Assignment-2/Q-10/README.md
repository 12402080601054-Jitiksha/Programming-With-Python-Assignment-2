# Q10: Python Data Visualization Dashboard Exporter

## 1. Objective

To develop a Python program that reads student marks from a CSV file, handles missing and invalid marks, calculates subject-wise statistics, and exports three visualization charts.

## 2. Requirements

- Python 3.10 or above
- pandas
- matplotlib
- A CSV file containing enrollment, name, and subject marks

Install dependencies:

```bash
python -m pip install pandas matplotlib
```

## 3. Files

- `12402080601054_Assignment2_Q10.py` — Main Python program
- `marks.csv` — Input dataset
- `cleaned_marks.csv` — Dataset after cleaning
- `summary.csv` — Subject-wise statistical summary
- `grade_distribution.png` — Grade distribution chart
- `subject_average.png` — Subject average comparison chart
- `top_performers.png` — Top performers chart

## 4. Input Format

The CSV must contain `enrollment` and `name` columns followed by one or more subject columns.

Example:

```csv
enrollment,name,Python,DBMS,OS
101,Asha,85,90,88
102,Dev,76,80,75
103,Riya,95,92,96
104,Kabir,65,,70
```

Marks must be between 0 and 100. Empty, non-numeric, and out-of-range marks are treated as missing.

## 5. Execution

Run the program:

```bash
python 12402080601054_Assignment2_Q10.py
```

Enter the input CSV path and the output directory when prompted.

## 6. Data Cleaning

- Converts subject marks to numeric values.
- Treats invalid and out-of-range values as missing.
- Replaces missing marks with the corresponding subject's mean.
- Uses 0 when all marks for a subject are missing.
- Rounds cleaned marks to two decimal places.

## 7. Statistics and Visualizations

The program calculates the student count, average, median, minimum, maximum, and population standard deviation for each subject.

It exports three charts:
1. Grade distribution across all subject marks.
2. Subject-wise average marks comparison.
3. Top 10 students ranked by average marks.

Grades are assigned as follows: A = 90–100, B = 80–89, C = 70–79, D = 60–69, and F = below 60.

## 8. Test Cases

1. Complete dataset with missing marks: all five output files are generated.
2. Dataset without missing marks: marks remain unchanged.
3. Dataset containing invalid marks: invalid values are treated as missing.
4. Entire subject column missing: marks are replaced with zero.
5. Missing required columns: the program displays an error.

## 9. Complexity Analysis

Let `n` be the number of students and `s` the number of subjects.

- **Time complexity:** O(n × s) for cleaning and calculating statistics, plus sorting up to n students for the top performers chart.
- **Space complexity:** O(n × s), because the dataset and cleaned dataset are stored in memory.

The program supports up to 1,000,000 students and 20 subjects, subject to available system memory.

## 10. Limitations

The program uses pandas and stores the dataset in memory. A streaming implementation would be more memory-efficient for very large datasets.
