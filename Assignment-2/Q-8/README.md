# Q8. Matrix Path Optimizer with Dynamic Programming

## 1. Problem Statement

The Matrix Path Optimizer finds the maximum-score path from the top-left cell to the bottom-right cell of an `n × m` matrix.

The allowed moves are:
- Right
- Down
- Diagonally down-right

Some cells may be blocked and represented by `X`. Blocked cells cannot be included in a path.

The program calculates:
- The maximum achievable path score.
- The number of distinct paths that achieve the maximum score, modulo `1000000007`.

If no valid path exists, the program prints `IMPOSSIBLE`.

## 2. Technologies Used

- Python 3.10 or above
- Dynamic Programming
- Matrix Algorithms
- Lists and Iteration
- Modular Arithmetic
- Input Validation
- Exception Handling

## 3. Requirements

- Python 3.10 or above
- No external libraries required

## 4. Features

- Finds the maximum path score.
- Counts all paths that achieve the maximum score.
- Supports right, down, and diagonal down-right movements.
- Handles blocked cells represented by `X`.
- Supports negative integer scores.
- Uses modulo `1000000007` for path counting.
- Detects unreachable destinations.
- Validates matrix dimensions and cell values.
- Uses optimized dynamic programming with `O(m)` auxiliary space.

## 5. How to Run

1. Install Python 3.10 or above.
2. Create a folder named `Q-8`.
3. Create the Python file:

   `12402080601054_Assignment2_Q8.py`

4. Copy the solution code into the file.
5. Save the file.
6. Open the folder in VS Code.
7. Select **Terminal → New Terminal**.
8. Run the program:

   ```bash
   python 12402080601054_Assignment2_Q8.py
   ```

9. Enter the matrix dimensions followed by the matrix rows.

## 6. Input Format

- First line: Two integers `n` and `m`, representing the number of rows and columns.
- Next `n` lines: Each line contains exactly `m` values.
- Each value is either an integer score or `X` for a blocked cell.

Example:

```text
3 3
1 2 3
4 X 6
7 8 9
```

## 7. Output Format

If a valid path exists, print two values separated by a space:

`maximum_score number_of_maximum_score_paths`

If no valid path exists, print:

`IMPOSSIBLE`

Example output:

```text
29 1
```

## 8. Algorithm

1. Read and validate the matrix dimensions.
2. Read the matrix and identify blocked cells.
3. Initialize the previous row's score array to negative infinity and its path-count array to zero.
4. Process the matrix row by row.
5. For each unblocked cell, consider valid paths from the left, above, and upper-left diagonal.
6. Select the predecessor with the highest score.
7. Add the current cell's score to the best predecessor score.
8. If multiple predecessors have the same maximum score, add their path counts modulo `1000000007`.
9. Store the current row's scores and path counts for the next iteration.
10. After processing all rows, check the bottom-right cell.
11. Print `IMPOSSIBLE` if it is unreachable; otherwise, print its maximum score and path count.

## 9. Complexity Analysis

**Time Complexity:** `O(n × m)`, because each cell is processed once and at most three predecessor cells are checked.

**Auxiliary Space Complexity:** `O(m)`, because only two rows of scores and path counts are maintained.

**Total Space Complexity:** `O(n × m)` in this implementation because the input matrix is stored in memory.

## 10. Test Cases

### Test Case 1: Sample Input

**Input:**

```text
3 3
1 2 3
4 X 6
7 8 9
```

**Expected Output:**

```text
29 1
```

**Explanation:** The maximum-score path is `1 → 4 → 7 → 8 → 9`, with a total score of 29.

### Test Case 2: Multiple Maximum-Score Paths

**Input:**

```text
2 2
0 0
0 0
```

**Expected Output:**

```text
0 3
```

**Explanation:** There are three distinct paths with the same maximum score: right then down, down then right, and diagonally down-right.

### Test Case 3: No Valid Path

**Input:**

```text
3 3
1 X 3
X X 4
5 6 7
```

**Expected Output:**

```text
IMPOSSIBLE
```

**Explanation:** Blocked cells prevent the destination from being reached.

### Test Case 4: Single Negative Cell

**Input:**

```text
1 1
-5
```

**Expected Output:**

```text
-5 1
```

**Explanation:** The only valid path consists of the single cell.

## 11. Input Validation and Assumptions

- `1 <= n, m <= 2000`
- Each cell contains an integer from `-1000000` to `1000000`, or `X`.
- Every matrix row must contain exactly `m` values.
- The top-left and bottom-right cells must be unblocked for a valid path.
- A path may use only right, down, or diagonal down-right movements.
- The path count is calculated modulo `1000000007`.
- Negative scores are allowed, so unreachable cells must be distinguished from valid negative-score paths.
