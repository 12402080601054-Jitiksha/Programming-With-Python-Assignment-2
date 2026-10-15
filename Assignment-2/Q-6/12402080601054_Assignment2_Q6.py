
import re
import sys
from collections import Counter, deque


LOG_PATTERN = re.compile(
    r"^(\d{2}):(\d{2})\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$"
)


def parse_log_line(line):
    """Parse and validate one timestamped log entry."""
    match = LOG_PATTERN.fullmatch(line.strip())

    if not match:
        raise ValueError(
            f"Invalid log format: {line.strip()}"
        )

    hour, minute, user, ip, status = match.groups()
    hour = int(hour)
    minute = int(minute)

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Invalid timestamp: {hour:02}:{minute:02}")

    timestamp = hour * 60 + minute
    return timestamp, f"{hour:02}:{minute:02}", user, ip, status


def detect_suspicious_users(x, window, n, input_stream):
    """
    Detect users with at least x failures in the previous
    window minutes followed by success from a different IP.

    Each user's deque stores (timestamp_in_minutes, IP).
    A Counter tracks the IPs of active failed attempts.
    """
    failure_queues = {}
    failure_ip_counts = {}
    suspicious_users = {}

    previous_timestamp = -1

    for _ in range(n):
        line = input_stream.readline()

        if not line:
            raise ValueError("Insufficient log entries.")

        timestamp, time_text, user, ip, status = parse_log_line(line)

        # Logs must be sorted by timestamp.
        if timestamp < previous_timestamp:
            raise ValueError("Logs must be sorted by timestamp.")

        previous_timestamp = timestamp

        if user not in failure_queues:
            failure_queues[user] = deque()
            failure_ip_counts[user] = Counter()

        queue = failure_queues[user]
        ip_counts = failure_ip_counts[user]

        # Remove failures that fall outside the sliding window.
        while queue and timestamp - queue[0][0] > window:
            old_timestamp, old_ip = queue.popleft()
            ip_counts[old_ip] -= 1

            if ip_counts[old_ip] == 0:
                del ip_counts[old_ip]

        if status == "FAIL":
            queue.append((timestamp, ip))
            ip_counts[ip] += 1

        elif status == "SUCCESS":
            # Save only the first suspicious success per user.
            if (
                user not in suspicious_users
                and len(queue) >= x
                and ip not in ip_counts
            ):
                suspicious_users[user] = time_text

    return suspicious_users


def main():
    try:
        # Read X and T.
        first_line = sys.stdin.readline().split()

        if len(first_line) != 2:
            raise ValueError("First line must contain X and T.")

        x, window = map(int, first_line)

        if not (1 <= x <= 100):
            raise ValueError("X must be between 1 and 100.")

        if not (1 <= window <= 1440):
            raise ValueError("T must be between 1 and 1440.")

        # Read number of log entries.
        second_line = sys.stdin.readline().strip()

        if not second_line or not second_line.isdigit():
            raise ValueError("Number of log entries must be an integer.")

        n = int(second_line)

        if not (1 <= n <= 2_000_000):
            raise ValueError("n must be between 1 and 2000000.")

        suspicious_users = detect_suspicious_users(
            x, window, n, sys.stdin
        )

        # Print user IDs in lexicographical order.
        if suspicious_users:
            for user in sorted(suspicious_users):
                print(user, suspicious_users[user])
        else:
            print("No suspicious users found.")

    except (ValueError, OverflowError) as error:
        print(f"Input error: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
