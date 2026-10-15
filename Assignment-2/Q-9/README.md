# Q9. OOP Inventory Merger with Operator Overloading

## 1. Problem Statement

Design an inventory management system using Python object-oriented programming.

The system contains `Product` and `Inventory` classes and supports adding, deleting, and updating products. It can also compare two inventories by their total selling value and merge inventories using operator overloading.

When two products have the same product ID:
- Their stock quantities are added.
- The lower purchase price is retained.
- The higher selling price is retained.
- The product name from the first inventory is preserved.

## 2. Technologies Used

- Python 3.10 or above
- Object-Oriented Programming
- Operator Overloading
- Dictionaries
- JSON File Handling
- Exception Handling
- Input Validation

## 3. Requirements

- Python 3.10 or above
- No external libraries required
- Two inventory JSON files

## 4. Features

- Add products to an inventory.
- Delete products by product ID.
- Update product stock.
- Merge two inventories using the overloaded `+` operator.
- Compare inventories using their total selling value.
- Load inventory data from JSON files.
- Save inventory data to a JSON file using the provided method.
- Handle duplicate product IDs and invalid values.
- Display merged products in sorted order.

## 5. How to Run

1. Install Python 3.10 or above.
2. Create a folder named `Q-9`.
3. Create the file `12402080601054_Assignment2_Q9.py`.
4. Copy the Python solution into the file.
5. Create `inventory_a.json` and `inventory_b.json`.
6. Open the folder in VS Code.
7. Select **Terminal → New Terminal**.
8. Run:

   ```bash
   python 12402080601054_Assignment2_Q9.py
   ```

9. Enter the paths of both inventory files.
10. Enter the number of operations and then the requested commands.

## 6. Input Format

The program first asks for the paths of the two inventory JSON files, followed by the number of operations.

Supported operations:

- `ADD A product_id "name" stock purchase selling`
- `DELETE A product_id`
- `UPDATE A product_id new_stock`
- `MERGE`
- `COMPARE A B`

Inventory names may be `A`, `B`, or `C`. Inventory `C` is created by the merge operation.

## 7. JSON File Format

Each inventory file contains a JSON list of products.

Example:

```json
[
  {
    "product_id": "P1",
    "name": "Pen",
    "stock": 10,
    "purchase_price": 5,
    "selling_price": 8
  }
]
```

Each product contains its ID, name, stock, purchase price, and selling price.

## 8. Output Format

The program displays an operation status, comparison results, or the merged inventory summary.

Example:

```text
MERGE successful.
P1 Pen stock=17 purchase=4 selling=9
Total valuation=153
```

Total valuation is calculated as:

`sum(stock × selling_price)`

## 9. Algorithm

1. Define the `Product` class with product details and validation.
2. Define the `Inventory` class with a dictionary keyed by product ID.
3. Implement methods to add, delete, and update products.
4. Overload the `+` operator using `__add__()` to merge inventories.
5. Combine stock for conflicting product IDs.
6. Preserve the minimum purchase price and maximum selling price.
7. Overload comparison operators to compare total inventory values.
8. Read inventory records from JSON files.
9. Execute user-specified operations.
10. Display results and operation status.

## 10. Complexity Analysis

Let `n` and `m` be the numbers of products in the two inventories.

- Add, delete, and update: `O(1)` average dictionary operation.
- Merge: `O(n + m)` average time.
- Compare total values: `O(n + m)` because totals are calculated by iterating over both inventories.
- Display sorted inventory: `O(k log k)`, where `k` is the number of products.
- Space complexity of merging: `O(n + m)`.

## 11. Test Cases

### Test Case 1: Merge Conflicting Products

Inventory A contains `P1 Pen 10 5 8`.

Inventory B contains `P1 Pen 7 4 9`.

**Expected output:**

```text
MERGE successful.
P1 Pen stock=17 purchase=4 selling=9
Total valuation=153
```

### Test Case 2: Add Product

**Operation:**

```text
ADD A P2 "Notebook" 20 15 25
```

**Expected output:**

```text
ADD successful.
```

### Test Case 3: Update Stock

**Operation:**

```text
UPDATE A P1 15
```

**Expected output:**

```text
UPDATE successful.
```

### Test Case 4: Compare Inventories

**Operation:**

```text
COMPARE A B
```

**Expected output:**

```text
A has greater total value.
A valuation=80
B valuation=63
```

## 12. Input Validation and Assumptions

- Product IDs and names must not be empty.
- Stock and prices must be non-negative integers.
- Values must fit within the signed 64-bit non-negative range.
- Product IDs must be unique within each inventory.
- JSON files must contain valid product records.
- Total inventory value is based on selling price.
- When product IDs conflict, the name from the first inventory is retained.
- Merge operations create a new inventory rather than modifying the original inventories.

