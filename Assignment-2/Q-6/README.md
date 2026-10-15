# Q6. Log Anomaly Detector Using Sliding Window

## 1. Problem Statement

The Log Anomaly Detector analyzes timestamped application logs to identify suspicious users.

A user is considered suspicious when:
- The user has at least `X` failed login attempts within a `T`-minute window.
- A successful login occurs after these failed attempts.
- The successful login comes from an IP address different from all IP addresses in the active failed-login window.

The program displays suspicious user IDs in lexicographical order along with the timestamp of their first detected suspicious success.

## 2. Technologies Used

- Python 3.10 or above
- Regular Expressions (`re`)
- Deque (`collections.deque`)
- Counter (`collections.Counter`)
- Dictionary (`dict`)
- Sliding Window Algorithm

## 3. Requirements

- Python 3.10 or above
- No external libraries required

## 4. Features

- Parses and validates log entries using regular expressions.
- Maintains a separate sliding window for each user.
- Removes failed attempts that fall outside the specified time window.
- Tracks failed login IP addresses efficiently.
- Detects suspicious successful logins from different IP addresses.
- Records the first suspicious success for each user.
- Displays suspicious users in lexicographical order.
- Handles malformed input and unsorted logs.
- Uses queues to avoid repeatedly scanning all historical log entries.

## 5. How to Run

1. Install Python 3.10 or above.
2. Create a folder named `Q-6`.
3. Create the Python file:

   `12402080601054_Assignment2_Q6.py`

4. Paste the solution code into the file.
5. Save the file.
6. Open the folder in VS Code.
7. Open the terminal using **Terminal → New Terminal**.
8. Run the program:

   ```bash
   python 12402080601054_Assignment2_Q6.py
   ```

9. Enter the input in the required format.

## 6. Input Format

- First line: Two integers `X` and `T`.
- Second line: Integer `n`, representing the number of log entries.
- Next `n` lines: Each line contains a timestamp, user ID, IP address, and login status.

Example:

```text
3 10
5
00:00 u1 1.1.1.1 FAIL
00:03 u1 1.1.1.1 FAIL
00:05 u1 1.1.1.1 FAIL
00:07 u1 2.2.2.2 SUCCESS
00:08 u2 3.3.3.3 SUCCESS
```

## 7. Output Format

The program prints suspicious user IDs in lexicographical order, followed by the timestamp of their first detected suspicious success.

Expected output:

```text
u1 00:07
```

If no suspicious users are detected, the program prints:

```text
No suspicious users found.
```

## 8. Algorithm

1. Read the threshold `X`, time window `T`, and number of log entries `n`.
2. Validate the input values.
3. Parse each log entry using a regular expression.
4. Convert the timestamp into minutes for easy comparison.
5. Maintain a deque of failed login timestamps and IP addresses for each user.
6. Remove failed attempts older than the current `T`-minute window.
7. Add new failed attempts to the user's deque and update the IP counter.
8. When a successful login occurs, check whether at least `X` failures remain in the window.
9. Check whether the successful login IP differs from all IPs in the active failure window.
10. Record the first suspicious success for each user.
11. Sort the suspicious user IDs and display their timestamps.

## 9. Complexity Analysis

**Time Complexity:**

- Processing logs: `O(n)` amortized, because each failed attempt is added to and removed from a deque at most once.
- Sorting suspicious users: `O(k log k)`, where `k` is the number of suspicious users.
- Total: `O(n + k log k)`.

**Space Complexity:**

`O(F + U)`, where `F` is the number of failed attempts retained in active windows and `U` is the number of tracked users.

## 10. Test Cases

### Test Case 1: Suspicious Login Detected

**Input:**

```text
3 10
5
00:00 u1 1.1.1.1 FAIL
00:03 u1 1.1.1.1 FAIL
00:05 u1 1.1.1.1 FAIL
00:07 u1 2.2.2.2 SUCCESS
00:08 u2 3.3.3.3 SUCCESS
```

**Expected Output:**

```text
u1 00:07
```

**Explanation:** User `u1` has three failed attempts within the time window, followed by a successful login from a different IP.

### Test Case 2: Same IP Address

**Input:**

```text
2 10
3
00:00 u1 1.1.1.1 FAIL
00:03 u1 1.1.1.1 FAIL
00:05 u1 1.1.1.1 SUCCESS
```

**Expected Output:**

```text
No suspicious users found.
```

**Explanation:** The successful login uses an IP address already present among the active failed attempts.

### Test Case 3: Insufficient Failed Attempts

**Input:**

```text
3 10
3
00:00 u1 1.1.1.1 FAIL
00:02 u1 1.1.1.1 FAIL
00:04 u1 2.2.2.2 SUCCESS
```

**Expected Output:**

```text
No suspicious users found.
```

**Explanation:** The user has only two failed attempts, but the required threshold is three.

### Test Case 4: Sliding Window Expiration

**Input:**

```text
2 5
3
00:00 u1 1.1.1.1 FAIL
00:02 u1 1.1.1.1 FAIL
00:08 u1 2.2.2.2 SUCCESS
```

**Expected Output:**

```text
No suspicious users found.
```

**Explanation:** The failure at `00:00` is outside the five-minute window when the success occurs at `00:08`. Only one active failed attempt remains.

## 11. Input Validation and Assumptions

- `1 <= n <= 2000000`
- `1 <= X <= 100`
- `1 <= T <= 1440`
- Timestamps must use the `HH:MM` format.
- Logs must be sorted by timestamp.
- Login statuses must be `FAIL` or `SUCCESS`.
- Timestamps are assumed to belong to the same day.
- The successful login IP must not match any IP in the active failed-login window.
- Each suspicious user is printed only once, using their first detected suspicious success.

## 12. GitHub Submission

1. Open GitHub and create a repository named `Assignment-2-Q6`.
2. Upload `12402080601054_Assignment2_Q6.py`.
3. Upload `README.md`.
4. Commit the files.
5. Open the repository and copy its URL.
6. Submit the repository link according to your instructor's instructions.

**Files to submit:**

- `12402080601054_Assignment2_Q6.py`
- `README.md`
- Test input/output evidence or screenshots, if required by your instructor.
