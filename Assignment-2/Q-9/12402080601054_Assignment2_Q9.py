
import json
import shlex
import sys
from pathlib import Path

MAX_VALUE = 2**63 - 1


class Product:
    """Represent a product in an inventory."""

    def __init__(self, product_id, name, stock, purchase_price, selling_price):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.selling_price = selling_price

    def validate(self):
        if not self.product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty.")

        for field, value in (
            ("stock", self.stock),
            ("purchase price", self.purchase_price),
            ("selling price", self.selling_price),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{field.capitalize()} must be an integer.")
            if not 0 <= value <= MAX_VALUE:
                raise ValueError(
                    f"{field.capitalize()} must be between 0 and {MAX_VALUE}."
                )

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "stock": self.stock,
            "purchase_price": self.purchase_price,
            "selling_price": self.selling_price,
        }

    @classmethod
    def from_dict(cls, data):
        required = {
            "product_id", "name", "stock",
            "purchase_price", "selling_price"
        }
        if not isinstance(data, dict) or not required.issubset(data):
            raise ValueError("Invalid product record in inventory file.")

        product = cls(
            data["product_id"],
            data["name"],
            data["stock"],
            data["purchase_price"],
            data["selling_price"],
        )

        if not isinstance(product.product_id, str):
            raise ValueError("Product ID must be a string.")
        if not isinstance(product.name, str):
            raise ValueError("Product name must be a string.")

        product.validate()
        return product

    def __str__(self):
        return (
            f"{self.product_id} {self.name} "
            f"stock={self.stock} "
            f"purchase={self.purchase_price} "
            f"selling={self.selling_price}"
        )


class Inventory:
    """Manage products using a dictionary keyed by product ID."""

    def __init__(self, name="Inventory"):
        self.name = name
        self.products = {}

    def add_product(self, product):
        product.validate()

        if product.product_id in self.products:
            raise ValueError(
                f"Product ID '{product.product_id}' already exists."
            )

        self.products[product.product_id] = product

    def delete_product(self, product_id):
        if product_id not in self.products:
            raise ValueError(f"Product ID '{product_id}' not found.")

        del self.products[product_id]

    def update_stock(self, product_id, new_stock):
        if product_id not in self.products:
            raise ValueError(f"Product ID '{product_id}' not found.")

        if (
            isinstance(new_stock, bool)
            or not isinstance(new_stock, int)
            or not 0 <= new_stock <= MAX_VALUE
        ):
            raise ValueError("Stock must be a valid non-negative 64-bit integer.")

        self.products[product_id].stock = new_stock

    def total_value(self):
        """Total inventory selling value."""
        return sum(
            product.stock * product.selling_price
            for product in self.products.values()
        )

    def __lt__(self, other):
        if not isinstance(other, Inventory):
            return NotImplemented
        return self.total_value() < other.total_value()

    def __eq__(self, other):
        if not isinstance(other, Inventory):
            return NotImplemented
        return self.total_value() == other.total_value()

    def __add__(self, other):
        """Merge inventories, combining conflicting product IDs."""
        if not isinstance(other, Inventory):
            return NotImplemented

        merged = Inventory(f"{self.name}+{other.name}")

        # Copy the first inventory so the original is not modified.
        for product in self.products.values():
            merged.products[product.product_id] = Product(
                product.product_id,
                product.name,
                product.stock,
                product.purchase_price,
                product.selling_price,
            )

        for product in other.products.values():
            if product.product_id not in merged.products:
                merged.products[product.product_id] = Product(
                    product.product_id,
                    product.name,
                    product.stock,
                    product.purchase_price,
                    product.selling_price,
                )
                continue

            existing = merged.products[product.product_id]

            # Check stock addition for 64-bit overflow.
            combined_stock = existing.stock + product.stock
            if combined_stock > MAX_VALUE:
                raise ValueError(
                    f"Merged stock exceeds the allowed range for "
                    f"{product.product_id}."
                )

            existing.stock = combined_stock
            existing.purchase_price = min(
                existing.purchase_price, product.purchase_price
            )
            existing.selling_price = max(
                existing.selling_price, product.selling_price
            )

            # Keep the existing name from the first inventory.

        return merged

    def display(self):
        for product_id in sorted(self.products):
            print(self.products[product_id])

        print(f"Total valuation={self.total_value()}")

    def save_to_file(self, file_path):
        data = [
            self.products[product_id].to_dict()
            for product_id in sorted(self.products)
        ]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load_from_file(cls, file_path, inventory_name):
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"Inventory file not found: {file_path}")

        inventory = cls(inventory_name)

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory JSON must contain a list of products.")

        for item in data:
            product = Product.from_dict(item)
            inventory.add_product(product)

        return inventory



def execute_operation(parts, inventories):
    """Execute one operation parsed using shell-style quoting."""
    if not parts:
        return

    operation = parts[0].upper()

    if operation == "ADD":
        if len(parts) != 7:
            raise ValueError(
                'Usage: ADD A product_id "name" stock purchase selling'
            )

        inventory_name, product_id, name = parts[1:4]
        stock, purchase, selling = map(int, parts[4:7])

        if inventory_name not in inventories:
            raise ValueError("Inventory must be A, B, or C.")

        inventories[inventory_name].add_product(
            Product(product_id, name, stock, purchase, selling)
        )
        print("ADD successful.")

    elif operation == "DELETE":
        if len(parts) != 3:
            raise ValueError("Usage: DELETE A product_id")

        inventory_name, product_id = parts[1:3]

        if inventory_name not in inventories:
            raise ValueError("Inventory must be A, B, or C.")

        inventories[inventory_name].delete_product(product_id)
        print("DELETE successful.")

    elif operation == "UPDATE":
        if len(parts) != 4:
            raise ValueError("Usage: UPDATE A product_id new_stock")

        inventory_name, product_id = parts[1:3]
        new_stock = int(parts[3])

        if inventory_name not in inventories:
            raise ValueError("Inventory must be A, B, or C.")

        inventories[inventory_name].update_stock(product_id, new_stock)
        print("UPDATE successful.")

    elif operation == "MERGE":
        if len(parts) != 1:
            raise ValueError("Usage: MERGE")

        inventories["C"] = inventories["A"] + inventories["B"]
        print("MERGE successful.")
        inventories["C"].display()

    elif operation == "COMPARE":
        if len(parts) != 3:
            raise ValueError("Usage: COMPARE A B")

        first, second = parts[1:3]

        if first not in inventories or second not in inventories:
            raise ValueError("Inventory must be A, B, or C.")

        value_a = inventories[first].total_value()
        value_b = inventories[second].total_value()

        if value_a > value_b:
            print(f"{first} has greater total value.")
        elif value_a < value_b:
            print(f"{second} has greater total value.")
        else:
            print("Inventories have equal total value.")

        print(f"{first} valuation={value_a}")
        print(f"{second} valuation={value_b}")

    else:
        raise ValueError(f"Unknown operation: {operation}")

def main():
    try:
        file_a = input("Enter path of inventory A JSON file: ").strip()
        file_b = input("Enter path of inventory B JSON file: ").strip()

        inventory_a = Inventory.load_from_file(file_a, "A")
        inventory_b = Inventory.load_from_file(file_b, "B")

        inventories = {"A": inventory_a, "B": inventory_b}

        q_text = input("Enter number of operations: ").strip()
        q = int(q_text)

        if not 1 <= q <= 300_000:
            raise ValueError("q must be between 1 and 300000.")

        print(
            'Operations: ADD A id "name" stock purchase selling; '
            'DELETE A id; UPDATE A id stock; MERGE; COMPARE A B'
        )

        for _ in range(q):
            line = input().strip()

            try:
                parts = shlex.split(line)
                execute_operation(parts, inventories)
            except (ValueError, KeyError, OverflowError) as error:
                print(f"Operation error: {error}")

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Input error: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
