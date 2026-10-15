# Q7. Generator-Based JSON ETL Pipeline

## 1. Problem Statement

The Generator-Based JSON ETL Pipeline processes large JSON Lines (JSONL) files containing sensor readings.

The program extracts sensor records, validates and transforms the data, filters corrupted records, and calculates summary statistics for each device.

For every device, the output includes:
- Total number of valid readings
- Minimum temperature
- Maximum temperature
- Average temperature
- Number of corrupted records

The pipeline uses generator functions to process records one at a time without loading the entire file into memory.

## 2. Technologies Used

- Programming Language: Python 3.10 or above
- JSON (`json`)
- Generators and Iterators
- File Handling
- Exception Handling
- Dictionaries and `defaultdict`
- Mathematical functions (`math`)
- Path handling (`pathlib`)

## 3. Requirements

- Python 3.10 or above
- No external libraries required
- Input file in JSON Lines format (`.jsonl`)

## 4. Features

- Reads JSONL files line by line.
- Uses generator functions for memory-efficient processing.
- Validates sensor readings and required fields.
- Detects invalid JSON and corrupted sensor records.
- Converts temperature values to numeric Celsius values.
- Converts humidity percentages into fractions during transformation.
- Groups sensor readings by device ID.
- Calculates count, minimum, maximum, and average temperature.
- Tracks corrupted records for each identifiable device.
- Reports corrupted records that cannot be assigned to a device separately.
- Displays device summaries in sorted order.
- Handles missing files and invalid input.

## 5. How to Run

1. Install Python 3.10 or above.
2. Create a folder named `Q-7`.
3. Create the Python file:

   `12402080601054_Assignment2_Q7.py`

4. Copy the solution code into the Python file.
5. Create the test input file named `test1.jsonl` or use another JSONL file.
6. Open the folder in VS Code.
7. Open the terminal using **Terminal → New Terminal**.
8. Run the program:

   ```bash
   python 12402080601054_Assignment2_Q7.py
   ```

9. Enter the JSONL file path when prompted.

Example:

```text
Enter JSONL file path: test1.jsonl
```

## 6. Input Format

The program accepts the path of a JSON Lines file.

Each line contains a JSON object with the following fields:

- `device_id`: String identifying the sensor device.
- `timestamp`: Optional timestamp string; if provided, it must not be empty.
- `temperature_c`: Numeric temperature in Celsius.
- `humidity`: Numeric humidity percentage between 0 and 100.

Example input file:

```jsonl
{"device_id":"D1","temperature_c":30,"humidity":50}
{"device_id":"D1","temperature_c":"bad","humidity":45}
{"device_id":"D2","temperature_c":25,"humidity":60}
```

## 7. Output Format

For each device, the program displays:

`device_id count=... min=... max=... avg=... corrupted=...`

Example output:

```text
D1 count=1 min=30 max=30 avg=30.00 corrupted=1
D2 count=1 min=25 max=25 avg=25.00 corrupted=0
```

If a corrupted record does not contain a valid device ID, it is counted separately:

```text
Unassigned corrupted records=1
```

If a device has no valid readings, its temperature statistics are displayed as `N/A`.

## 8. Algorithm

1. Accept the path of the JSONL input file.
2. Check whether the file exists.
3. Read the file one line at a time using a generator.
4. Parse each line using the JSON module.
5. Validate the JSON structure and required sensor fields.
6. Identify corrupted records and track their counts.
7. Normalize valid temperature values to numeric Celsius.
8. Convert humidity percentages into fractions.
9. Group readings by device using a dictionary.
10. Update each device's count, minimum temperature, maximum temperature, and temperature sum.
11. Calculate the average temperature for each device.
12. Display the summary statistics in sorted device order.

## 9. Complexity Analysis

**Time Complexity:** `O(n + d log d)`, where `n` is the number of records and `d` is the number of devices. Processing each record takes constant expected time, while sorting device IDs takes `O(d log d)` time.

**Space Complexity:** `O(d)`, where `d` is the number of devices stored in the aggregation dictionary. The complete input file is not stored in memory.

## 10. Test Cases

### Test Case 1: Sample Input

**Input:**

```jsonl
{"device_id":"D1","temperature_c":30,"humidity":50}
{"device_id":"D1","temperature_c":"bad","humidity":45}
```

**Expected Output:**

```text
D1 count=1 min=30 max=30 avg=30.00 corrupted=1
```

**Explanation:** The first reading is valid. The second reading is corrupted because its temperature is not numeric.

### Test Case 2: Multiple Valid Readings

**Input:**

```jsonl
{"device_id":"D1","temperature_c":20,"humidity":40}
{"device_id":"D1","temperature_c":30,"humidity":60}
{"device_id":"D2","temperature_c":25,"humidity":50}
```

**Expected Output:**

```text
D1 count=2 min=20 max=30 avg=25.00 corrupted=0
D2 count=1 min=25 max=25 avg=25.00 corrupted=0
```

**Explanation:** The program calculates separate statistics for each device.

### Test Case 3: Missing and Invalid Fields

**Input:**

```jsonl
{"device_id":"D1","temperature_c":22,"humidity":45}
{"device_id":"D1","temperature_c":24}
{"device_id":"D1","temperature_c":26,"humidity":120}
{"device_id":"D2","temperature_c":28,"humidity":55}
```

**Expected Output:**

```text
D1 count=1 min=22 max=22 avg=22.00 corrupted=2
D2 count=1 min=28 max=28 avg=28.00 corrupted=0
```

**Explanation:** The second record is missing humidity, and the third contains an out-of-range humidity value.

### Test Case 4: Invalid JSON Record

**Input:**

```jsonl
{"device_id":"D1","temperature_c":18,"humidity":40}
this is not valid JSON
{"device_id":"D2","temperature_c":26,"humidity":50}
```

**Expected Output:**

```text
D1 count=1 min=18 max=18 avg=18.00 corrupted=0
D2 count=1 min=26 max=26 avg=26.00 corrupted=0
Unassigned corrupted records=1
```

**Explanation:** The invalid JSON line cannot be associated with a device, so it is counted separately.

## 11. Limitations and Assumptions

- The input must be a JSON Lines file, with one JSON object per line.
- `device_id`, `temperature_c`, and `humidity` are required.
- The timestamp is optional to accommodate the assignment's sample input.
- Temperature values must be finite numbers.
- Humidity must be a finite number between 0 and 100.
- Temperature statistics are reported in Celsius to match the provided sample output.
- Corrupted records with valid device IDs are included in that device's corrupted count.
- Corrupted records without valid device IDs are counted separately.
- Memory usage depends on the number of distinct devices rather than the total file size.
