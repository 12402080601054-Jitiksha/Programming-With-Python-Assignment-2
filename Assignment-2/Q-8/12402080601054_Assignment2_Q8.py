
import sys

MOD = 1_000_000_007
NEG_INF = float("-inf")


def find_maximum_path(matrix, n, m):
    """
    Return (maximum_score, number_of_maximum_paths).

    Allowed moves:
    - Right
    - Down
    - Diagonally down-right

    Uses O(m) auxiliary space.
    """
    # Previous row's best scores and path counts.
    prev_score = [NEG_INF] * m
    prev_count = [0] * m

    for i in range(n):
        curr_score = [NEG_INF] * m
        curr_count = [0] * m

        for j in range(m):
            cell = matrix[i][j]

            # Blocked cells cannot be part of a valid path.
            if cell is None:
                continue

            # Starting cell.
            if i == 0 and j == 0:
                curr_score[j] = cell
                curr_count[j] = 1
                continue

            best_score = NEG_INF
            ways = 0

            # From the left (move right).
            if j > 0 and curr_score[j - 1] != NEG_INF:
                best_score = curr_score[j - 1]
                ways = curr_count[j - 1]

            # From above (move down).
            if prev_score[j] != NEG_INF:
                if prev_score[j] > best_score:
                    best_score = prev_score[j]
                    ways = prev_count[j]
                elif prev_score[j] == best_score:
                    ways = (ways + prev_count[j]) % MOD

            # From upper-left (move diagonally down-right).
            if j > 0 and prev_score[j - 1] != NEG_INF:
                if prev_score[j - 1] > best_score:
                    best_score = prev_score[j - 1]
                    ways = prev_count[j - 1]
                elif prev_score[j - 1] == best_score:
                    ways = (ways + prev_count[j - 1]) % MOD

            # Only reachable cells receive a score and path count.
            if best_score != NEG_INF:
                curr_score[j] = best_score + cell
                curr_count[j] = ways % MOD

        prev_score = curr_score
        prev_count = curr_count

    if prev_score[m - 1] == NEG_INF:
        return None

    return prev_score[m - 1], prev_count[m - 1]


def main():
    try:
        first_line = sys.stdin.readline().split()

        if len(first_line) != 2:
            raise ValueError("First line must contain n and m.")

        n, m = map(int, first_line)

        if not (1 <= n <= 2000 and 1 <= m <= 2000):
            raise ValueError("n and m must be between 1 and 2000.")

        matrix = []

        for row_index in range(n):
            line = sys.stdin.readline()

            if not line:
                raise ValueError("Not enough matrix rows.")

            values = line.split()

            if len(values) != m:
                raise ValueError(
                    f"Row {row_index + 1} must contain exactly {m} values."
                )

            row = []

            for value in values:
                if value == "X":
                    row.append(None)
                else:
                    try:
                        number = int(value)
                    except ValueError:
                        raise ValueError(
                            f"Invalid matrix value: {value}"
                        )

                    if not (-10**6 <= number <= 10**6):
                        raise ValueError(
                            "Cell values must be between -1000000 and 1000000."
                        )

                    row.append(number)

            matrix.append(row)

        # Both endpoints must be usable.
        if matrix[0][0] is None or matrix[n - 1][m - 1] is None:
            print("IMPOSSIBLE")
            return

        result = find_maximum_path(matrix, n, m)

        if result is None:
            print("IMPOSSIBLE")
        else:
            maximum_score, number_of_paths = result
            print(maximum_score, number_of_paths)

    except ValueError as error:
        print(f"Input error: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
