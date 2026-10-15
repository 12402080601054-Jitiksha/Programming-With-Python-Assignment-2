
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def read_jsonl(file_path):
    """Read a JSON Lines file one line at a time."""
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("Each JSON line must be an object.")
                yield line_number, record, None
            except (json.JSONDecodeError, ValueError) as error:
                yield line_number, None, str(error)


def is_valid_number(value):
    """Accept finite integers or floats, but reject booleans and strings."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def transform_records(records):
    """
    Validate and transform records.
    Temperature is normalized to a numeric Celsius value.
    Humidity is converted from percentage to a fraction.
    """
    for line_number, record, parse_error in records:
        if parse_error is not None:
            yield line_number, None, None, None, parse_error
            continue

        device_id = record.get("device_id")

        if not isinstance(device_id, str) or not device_id.strip():
            yield (
                line_number, None, None, None,
                "Missing or invalid device_id"
            )
            continue

        device_id = device_id.strip()
        temperature = record.get("temperature_c")
        humidity = record.get("humidity")

        # The sample does not contain timestamps, so timestamp is optional.
        # If provided, it must be a non-empty string.
        timestamp = record.get("timestamp")
        if timestamp is not None and (
            not isinstance(timestamp, str) or not timestamp.strip()
        ):
            yield (
                line_number, device_id, None, None,
                "Invalid timestamp"
            )
            continue

        if not is_valid_number(temperature):
            yield (
                line_number, device_id, None, None,
                "Invalid temperature_c"
            )
            continue

        if not is_valid_number(humidity) or not 0 <= humidity <= 100:
            yield (
                line_number, device_id, None, None,
                "Invalid humidity"
            )
            continue

        # Normalize numeric temperature and convert humidity % to a fraction.
        temperature_c = float(temperature)
        humidity_fraction = float(humidity) / 100.0

        yield (
            line_number, device_id, temperature_c,
            humidity_fraction, None
        )


def aggregate_records(transformed_records):
    """Aggregate readings and corrupted counts for each device."""
    statistics = defaultdict(
        lambda: {
            "count": 0,
            "min_temp": None,
            "max_temp": None,
            "temp_sum": 0.0,
            "corrupted": 0,
        }
    )

    unassigned_corrupted = 0

    for line_number, device_id, temperature, humidity, error in transformed_records:
        if error is not None:
            if device_id is None:
                # Cannot assign this record to a device.
                unassigned_corrupted += 1
            else:
                statistics[device_id]["corrupted"] += 1
            continue

        stats = statistics[device_id]
        stats["count"] += 1
        stats["temp_sum"] += temperature

        if stats["min_temp"] is None or temperature < stats["min_temp"]:
            stats["min_temp"] = temperature

        if stats["max_temp"] is None or temperature > stats["max_temp"]:
            stats["max_temp"] = temperature

    return statistics, unassigned_corrupted


def print_summary(statistics, unassigned_corrupted):
    """Print one summary line per device in sorted order."""
    for device_id in sorted(statistics):
        stats = statistics[device_id]
        count = stats["count"]

        if count > 0:
            average = stats["temp_sum"] / count
            min_temp = f"{stats['min_temp']:g}"
            max_temp = f"{stats['max_temp']:g}"
            avg_temp = f"{average:.2f}"
        else:
            min_temp = "N/A"
            max_temp = "N/A"
            avg_temp = "N/A"

        print(
            f"{device_id} count={count} "
            f"min={min_temp} max={max_temp} "
            f"avg={avg_temp} corrupted={stats['corrupted']}"
        )

    if unassigned_corrupted:
        print(f"Unassigned corrupted records={unassigned_corrupted}")


def main():
    """Read a JSONL path and run the streaming ETL pipeline."""
    try:
        file_path = input("Enter JSONL file path: ").strip()

        if not file_path:
            raise ValueError("File path cannot be empty.")

        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        records = read_jsonl(path)
        transformed = transform_records(records)
        statistics, unassigned_corrupted = aggregate_records(transformed)

        print_summary(statistics, unassigned_corrupted)

    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
