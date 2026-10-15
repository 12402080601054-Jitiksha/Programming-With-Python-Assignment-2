
# Assignment 2 - Q2: Offline Web Scraping Ranker from HTML Pages

## 1. Problem Statement

Develop a Python program that extracts product names, prices, and ratings
from multiple saved HTML files.

The program cleans the extracted data, removes duplicate products by name,
and displays the top K products according to these rules:

1. Higher rating comes first.
2. If ratings are equal, lower price comes first.
3. If both rating and price are equal, product name is sorted
   alphabetically.

## 2. Technologies Used

- Python 3.10 or above
- HTMLParser from html.parser
- Regular expressions using re
- Dictionaries and lists
- File handling
- Sorting and data cleaning

## 3. Requirements

- Python 3.10 or above
- No external libraries required
- Saved HTML files containing product information

## 4. Expected HTML Structure

Each product should be contained inside a div with class "product".

The product name, price, and rating must use the classes "name",
"price", and "rating", respectively.

Example:

```html
<div class="product">
  <span class="name">Python Book</span>
  <span class="price">₹499</span>
  <span class="rating">4.8</span>
</div>
```

## 5. How to Run

### Step 1: Verify Python

```bash
python --version
```

### Step 2: Open the project folder

Open Command Prompt or the VS Code terminal in the project directory.

### Step 3: Execute the program

```bash
python 12402080601054_Assignment2_Q2.py
```

### Step 4: Provide input

Enter the number of HTML files, K, and each file path.

Example:

```text
2 2
page1.html
page2.html
```

## 6. Input Format

The first line contains two integers P and K.

The next P lines contain paths to saved HTML files.

- P: Number of HTML files
- K: Number of top products to display

## 7. Output Format

Each output line contains:

```text
product_name normalized_price rating
```

## 8. Algorithm

1. Read P and K from standard input.
2. Validate the input values.
3. Read the paths of the HTML files.
4. Parse each HTML file using HTMLParser.
5. Extract product names, prices, and ratings.
6. Normalize whitespace in product names.
7. Remove currency symbols and commas from prices.
8. Convert ratings and prices into numeric values.
9. Ignore products with missing or invalid fields.
10. Remove duplicates using a dictionary keyed by normalized name.
11. Retain the highest-rated entry for each duplicate name.
12. For equal ratings, retain the lower-priced entry.
13. Sort by descending rating, ascending price, and ascending name.
14. Display the first K products.

## 9. Complexity Analysis

Let N be the total HTML size and U be the number of unique products.

Expected parsing time: O(N)

Sorting time: O(U log U)

Expected space complexity: O(U), excluding parser and file-buffer
overhead.

## 10. Test Cases

### Test Case 1: Duplicate products

Input:

```text
1 2
test1.html
```

Expected output:

```text
Python Book 499 4.8
USB Keyboard 799 4.7
```

### Test Case 2: Equal ratings

Input:

```text
1 3
test2.html
```

Expected output:

```text
Laptop Stand 500 4.9
USB Hub 300 4.5
Wireless Mouse 600 4.5
```

### Test Case 3: Equal rating and price

Input:

```text
1 3
test3.html
```

Expected output:

```text
Alpha Notebook 1200 4.6
Zebra Notebook 1200 4.6
Premium Pen 150 4.2
```

## 11. Limitations

- The parser expects the specified HTML class names.
- It works on saved HTML files and does not fetch webpages online.
- Duplicate products are identified by product name, ignoring case.
- Prices are interpreted as numeric values after removing commas
  and currency symbols.
- The program retains the best-rated, then lowest-priced record
  when duplicate product names have conflicting data.
