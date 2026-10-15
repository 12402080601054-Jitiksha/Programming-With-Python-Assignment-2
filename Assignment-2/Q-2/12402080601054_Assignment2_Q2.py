
import re
import sys
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


# HTML elements that do not have closing tags.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr"
}

# Common class/id keywords used in product listing pages.
CARD_KEYWORDS = {"product", "product-card", "product-item", "listing"}
NAME_KEYWORDS = {"name", "product-name", "title", "product-title"}
PRICE_KEYWORDS = {"price", "product-price", "current-price"}
RATING_KEYWORDS = {"rating", "product-rating", "stars"}


def get_keywords(attributes):
    """Return normalized class and id keywords from HTML attributes."""
    values = dict(attributes)
    result = set()

    for attribute in ("class", "id"):
        value = values.get(attribute, "")
        result.update(
            token.lower()
            for token in re.split(r"[\s_-]+", value)
            if token
        )
        # Also preserve the complete class/id value.
        if value:
            result.add(value.lower())

    return result


def normalize_price(price_text):
    """Convert a displayed price into a numeric Decimal value."""
    cleaned = price_text.strip()
    cleaned = re.sub(r"[₹$€£,\s]", "", cleaned)

    # Accept a number with an optional decimal part.
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", cleaned):
        return None

    try:
        price = Decimal(cleaned)
        if not price.is_finite() or price < 0:
            return None
        return price
    except InvalidOperation:
        return None


def format_price(price):
    """Display integral prices without unnecessary decimal zeros."""
    if price == price.to_integral_value():
        return str(int(price))
    return format(price.normalize(), "f")


class ProductHTMLParser(HTMLParser):
    """Extract products from HTML using common class and id names."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.current_product = None
        self.product_depth = None
        self.capture = None
        self.products = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.depth += 1

        keywords = get_keywords(attrs)

        # Start a new product card.
        if self.current_product is None and keywords & CARD_KEYWORDS:
            self.current_product = {
                "name": "",
                "price_text": "",
                "rating_text": ""
            }
            self.product_depth = self.depth

        if self.current_product is None:
            return

        # Identify which product field is being read.
        field = None
        if keywords & NAME_KEYWORDS:
            field = "name"
        elif keywords & PRICE_KEYWORDS:
            field = "price_text"
        elif keywords & RATING_KEYWORDS:
            field = "rating_text"

        if field is not None:
            self.capture = {
                "field": field,
                "depth": self.depth,
                "parts": []
            }

    def handle_data(self, data):
        if self.capture is not None:
            self.capture["parts"].append(data)

    def handle_endtag(self, tag):
        # Save captured text when its HTML element closes.
        if self.capture is not None and self.capture["depth"] == self.depth:
            value = " ".join("".join(self.capture["parts"]).split())
            field = self.capture["field"]

            if self.current_product is not None and value:
                self.current_product[field] = value

            self.capture = None

        # Finish the product card.
        if (
            self.current_product is not None
            and self.product_depth == self.depth
        ):
            self.products.append(self.current_product)
            self.current_product = None
            self.product_depth = None
            self.capture = None

        if tag not in VOID_TAGS:
            self.depth = max(0, self.depth - 1)

    def close(self):
        super().close()

        # Do not silently lose a final card if its closing tag is missing.
        if self.current_product is not None:
            self.products.append(self.current_product)
            self.current_product = None


def extract_products(file_path):
    """Parse one HTML file and return its valid product records."""
    parser = ProductHTMLParser()

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            for chunk in iter(lambda: file.read(65536), ""):
                parser.feed(chunk)

        parser.close()

    except (OSError, UnicodeError) as error:
        print(f"Warning: Cannot read {file_path}: {error}", file=sys.stderr)
        return []

    valid_products = []

    for item in parser.products:
        name = item["name"].strip()
        price = normalize_price(item["price_text"])

        rating_match = re.search(
            r"(?<!\d)(\d+(?:\.\d+)?)(?!\d)",
            item["rating_text"]
        )

        if not name or price is None or rating_match is None:
            continue

        try:
            rating = Decimal(rating_match.group(1))
        except InvalidOperation:
            continue

        if not rating.is_finite() or not Decimal("0") <= rating <= Decimal("5"):
            continue

        valid_products.append({
            "name": name,
            "price": price,
            "rating": rating
        })

    return valid_products


def rank_products(file_paths, k):
    """Deduplicate products and return the top K ranked products."""
    unique_products = {}

    for file_path in file_paths:
        for product in extract_products(file_path):
            name = product["name"]

            if name not in unique_products:
                unique_products[name] = product
            else:
                previous = unique_products[name]

                # For duplicate names, retain the better rating;
                # if ratings tie, retain the lower price.
                if (
                    product["rating"] > previous["rating"]
                    or (
                        product["rating"] == previous["rating"]
                        and product["price"] < previous["price"]
                    )
                ):
                    unique_products[name] = product

    ranked = sorted(
        unique_products.values(),
        key=lambda item: (
            -item["rating"],
            item["price"],
            item["name"]
        )
    )

    return ranked[:k]


def main():
    """Read input, validate it, and print the top K products."""
    first_line = sys.stdin.readline().strip().split()

    if len(first_line) != 2:
        print("Error: First line must contain p and k.")
        return

    try:
        p, k = map(int, first_line)
    except ValueError:
        print("Error: p and k must be integers.")
        return

    if not 1 <= p <= 5000 or not 1 <= k <= 1000:
        print("Error: p must be 1-5000 and k must be 1-1000.")
        return

    file_paths = []

    for _ in range(p):
        path = sys.stdin.readline().strip()

        if not path:
            print("Error: Missing HTML file path.")
            return

        if not Path(path).is_file():
            print(f"Error: File not found: {path}")
            return

        file_paths.append(path)

    products = rank_products(file_paths, k)

    for product in products:
        print(
            f"{product['name']} "
            f"{format_price(product['price'])} "
            f"{format_price(product['rating'])}"
        )


if __name__ == "__main__":
    main()
