"""
E-commerce Product Scraper - Complete Standalone Version
=========================================================

A fully self-contained Python scraper for extracting product details from e-commerce websites.
NO EXTERNAL APIs REQUIRED - uses only HTTP requests to scrape public HTML pages.

Requirements:
    pip install requests beautifulsoup4

Features:
- Extracts product name, price, description, images, and availability
- Supports JSON-LD structured data extraction (schema.org Product markup)
- Falls back to HTML parsing with BeautifulSoup for flexible site support
- Smart currency detection (USD, EUR, GBP, JPY, INR, etc.)
- Built-in test cases with sample HTML to verify functionality
- Ready to use - just copy and paste into your workflow

Usage:
    # As a script
    python ecommerce_scraper_complete.py

    # Or import in your code
    from ecommerce_scraper_complete import EcommerceProductScraper
    scraper = EcommerceProductScraper()
    result = scraper.scrape("https://example.com/product/123")
    print(result)
"""

import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print("ERROR: Missing required packages.")
    print("Please install: pip install requests beautifulsoup4")
    sys.exit(1)


class EcommerceProductScraper:
    """
    Self-contained e-commerce product scraper.
    NO EXTERNAL APIs - only scrapes public HTML pages.
    """

    def __init__(
        self,
        timeout: int = 30,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        max_images: int = 5,
    ):
        """
        Initialize the scraper.

        Args:
            timeout: Request timeout in seconds (default: 30)
            user_agent: User agent string for requests
            max_images: Maximum number of images to extract (default: 5)
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self.max_images = max_images

    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape product information from a URL.

        Args:
            url: The product page URL to scrape

        Returns:
            Dictionary containing:
            - name: Product name
            - price: Product price (numeric value as string)
            - currency: Currency code (USD, EUR, etc.)
            - description: Product description
            - images: List of image URLs
            - availability: Stock status
            - url: The scraped URL
            - error: Error message if scraping failed
        """
        result = {
            "url": url,
            "name": "",
            "price": "",
            "currency": "",
            "description": "",
            "images": [],
            "availability": "",
            "error": "",
        }

        try:
            # Fetch the page HTML
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            html_content = response.text

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Try JSON-LD first (most reliable for e-commerce sites)
            json_ld_data = self._extract_json_ld(soup)
            if json_ld_data:
                result = self._extract_from_json_ld(json_ld_data, result, url)

            # If JSON-LD didn't provide everything, use HTML parsing
            if not result["name"]:
                result["name"] = self._extract_name(soup)

            if not result["price"]:
                price_info = self._extract_price(soup)
                result["price"] = price_info["price"]
                if not result["currency"]:
                    result["currency"] = price_info["currency"]

            if not result["description"]:
                result["description"] = self._extract_description(soup)

            if not result["images"]:
                result["images"] = self._extract_images(soup, url)

            if not result["availability"]:
                result["availability"] = self._extract_availability(soup)

        except requests.Timeout:
            result["error"] = f"Request timeout after {self.timeout} seconds"
        except requests.RequestException as e:
            result["error"] = f"Request error: {str(e)}"
        except Exception as e:
            result["error"] = f"Scraping error: {str(e)}"

        return result

    def _extract_json_ld(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract JSON-LD structured data from the page."""
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)

                # Handle both single objects and arrays
                items = [data] if isinstance(data, dict) else data if isinstance(data, list) else []

                for item in items:
                    if not isinstance(item, dict):
                        continue

                    # Check for Product type
                    if item.get("@type") == "Product":
                        return item

                    # Check for Product in @graph
                    if "@graph" in item:
                        for graph_item in item["@graph"]:
                            if isinstance(graph_item, dict) and graph_item.get("@type") == "Product":
                                return graph_item

            except (json.JSONDecodeError, AttributeError):
                continue

        return {}

    def _extract_from_json_ld(
        self, json_ld: Dict[str, Any], result: Dict[str, Any], base_url: str
    ) -> Dict[str, Any]:
        """Extract product info from JSON-LD data."""
        if "name" in json_ld:
            result["name"] = json_ld["name"]

        if "description" in json_ld:
            result["description"] = json_ld["description"]

        # Extract price and currency from offers
        if "offers" in json_ld:
            offers = json_ld["offers"]
            # Handle both single offer and array of offers
            if isinstance(offers, dict):
                offers = [offers]
            if isinstance(offers, list) and offers:
                offer = offers[0]
                if "price" in offer:
                    result["price"] = str(offer["price"])
                if "priceCurrency" in offer:
                    result["currency"] = offer["priceCurrency"]
                if "availability" in offer:
                    avail = offer["availability"]
                    # Extract just the status part (e.g., "InStock" from "https://schema.org/InStock")
                    result["availability"] = avail.split("/")[-1] if "/" in avail else avail

        # Extract images
        if "image" in json_ld:
            images = json_ld["image"]
            if isinstance(images, str):
                result["images"] = [images]
            elif isinstance(images, list):
                result["images"] = images[: self.max_images]

        return result

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract product name from HTML."""
        # Try common selectors for product names
        selectors = [
            "h1[class*='product']",
            "h1[class*='title']",
            "h1[itemprop='name']",
            ".product-name",
            ".product-title",
            "#product-title",
            "h1",
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements and elements[0].get_text(strip=True):
                return elements[0].get_text(strip=True)

        return ""

    def _extract_price(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract product price and currency from HTML."""
        result = {"price": "", "currency": ""}

        # Try common selectors for product prices
        selectors = [
            "[class*='price'][class*='current']",
            "[class*='product-price']",
            "[itemprop='price']",
            ".price",
            "[class*='price']",
            "#price",
        ]

        price_text = ""
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for elem in elements:
                    text = elem.get_text(strip=True)
                    # Skip if it looks like a label (too short or no numbers)
                    if text and re.search(r"\d", text) and len(text) < 100:
                        price_text = text
                        break
                if price_text:
                    break

        if price_text:
            # Extract currency and numeric price
            result = self._parse_price_text(price_text)

        return result

    def _parse_price_text(self, price_text: str) -> Dict[str, str]:
        """Parse price text to extract numeric price and currency."""
        # Currency symbols and codes
        currency_map = {
            "$": "USD",
            "€": "EUR",
            "£": "GBP",
            "¥": "JPY",
            "₹": "INR",
            "₽": "RUB",
            "₩": "KRW",
            "¢": "USD",
            "USD": "USD",
            "EUR": "EUR",
            "GBP": "GBP",
            "CAD": "CAD",
            "AUD": "AUD",
        }

        currency = ""
        for symbol, code in currency_map.items():
            if symbol in price_text:
                currency = code
                break

        # Extract numeric price (handles formats like 1,234.56 or 1.234,56)
        price_match = re.search(r"(\d{1,3}(?:[,\.]\d{3})*(?:[,\.]\d{2})?)", price_text)
        price = price_match.group(1) if price_match else price_text

        return {"price": price, "currency": currency}

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract product description from HTML."""
        # Try common selectors for product descriptions
        selectors = [
            "[class*='product-description']",
            "[class*='description']",
            "[itemprop='description']",
            ".description",
            "#description",
            "[class*='product-details']",
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                text = elements[0].get_text(strip=True)
                # Return if we found substantial description text
                if len(text) > 20:
                    return text[:500]  # Limit to 500 chars

        return ""

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract product images from HTML."""
        images = []

        # Try common selectors for product images
        selectors = [
            "img[class*='product']",
            "img[itemprop='image']",
            ".product-image img",
            "[class*='gallery'] img",
            "[class*='product'] img",
        ]

        seen_urls = set()
        for selector in selectors:
            elements = soup.select(selector)
            for elem in elements:
                # Get image URL from src or data-src
                img_url = elem.get("src") or elem.get("data-src")
                if img_url:
                    # Convert relative URLs to absolute
                    img_url = urljoin(base_url, img_url)
                    # Skip duplicates and tiny images (likely icons)
                    if img_url not in seen_urls and not any(
                        x in img_url.lower() for x in ["icon", "logo", "sprite"]
                    ):
                        images.append(img_url)
                        seen_urls.add(img_url)
                        if len(images) >= self.max_images:
                            return images

        return images

    def _extract_availability(self, soup: BeautifulSoup) -> str:
        """Extract product availability/stock status from HTML."""
        # Try common selectors for availability
        selectors = [
            "[class*='availability']",
            "[class*='stock']",
            "[itemprop='availability']",
            ".stock-status",
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                text = elements[0].get_text(strip=True)
                if text:
                    return text

        return ""


# ============================================================================
# BUILT-IN TESTS - Verify the scraper works correctly
# ============================================================================


def run_tests():
    """Run comprehensive tests to verify the scraper works correctly."""
    print("=" * 80)
    print("RUNNING BUILT-IN TESTS")
    print("=" * 80)
    print()

    tests_passed = 0
    tests_failed = 0

    # Test 1: JSON-LD extraction
    print("Test 1: JSON-LD Extraction")
    print("-" * 40)
    test_html_json_ld = """
    <html>
    <head>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": "Premium Wireless Headphones",
            "description": "High-quality wireless headphones with noise cancellation",
            "image": "https://example.com/headphones.jpg",
            "offers": {
                "@type": "Offer",
                "price": "199.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock"
            }
        }
        </script>
    </head>
    <body></body>
    </html>
    """

    soup = BeautifulSoup(test_html_json_ld, "html.parser")
    scraper = EcommerceProductScraper()
    json_ld = scraper._extract_json_ld(soup)

    if json_ld and json_ld.get("name") == "Premium Wireless Headphones":
        print("✓ PASSED: JSON-LD product name extracted correctly")
        tests_passed += 1
    else:
        print("✗ FAILED: JSON-LD extraction failed")
        tests_failed += 1

    result = {"url": "test", "name": "", "price": "", "currency": "", "description": "", "images": [], "availability": ""}
    result = scraper._extract_from_json_ld(json_ld, result, "https://example.com")

    if result["price"] == "199.99" and result["currency"] == "USD":
        print("✓ PASSED: Price and currency extracted from JSON-LD")
        tests_passed += 1
    else:
        print(f"✗ FAILED: Price extraction (got {result['price']} {result['currency']})")
        tests_failed += 1

    print()

    # Test 2: HTML parsing (name)
    print("Test 2: HTML Name Extraction")
    print("-" * 40)
    test_html_name = """
    <html>
    <body>
        <h1 class="product-title">Amazing Smart Watch</h1>
    </body>
    </html>
    """

    soup = BeautifulSoup(test_html_name, "html.parser")
    name = scraper._extract_name(soup)

    if name == "Amazing Smart Watch":
        print("✓ PASSED: Product name extracted from HTML")
        tests_passed += 1
    else:
        print(f"✗ FAILED: Name extraction (got '{name}')")
        tests_failed += 1

    print()

    # Test 3: Price parsing
    print("Test 3: Price Parsing")
    print("-" * 40)
    test_cases = [
        ("$99.99", "99.99", "USD"),
        ("€49.50", "49.50", "EUR"),
        ("£29.99", "29.99", "GBP"),
        ("¥1,299", "1,299", "JPY"),
        ("1.234,56 EUR", "1.234,56", "EUR"),
    ]

    for price_text, expected_price, expected_currency in test_cases:
        parsed = scraper._parse_price_text(price_text)
        if parsed["price"] == expected_price and parsed["currency"] == expected_currency:
            print(f"✓ PASSED: '{price_text}' → {expected_price} {expected_currency}")
            tests_passed += 1
        else:
            print(f"✗ FAILED: '{price_text}' → got {parsed['price']} {parsed['currency']}")
            tests_failed += 1

    print()

    # Test 4: Description extraction
    print("Test 4: Description Extraction")
    print("-" * 40)
    test_html_desc = """
    <html>
    <body>
        <div class="product-description">
            This is a detailed description of an amazing product with many features.
        </div>
    </body>
    </html>
    """

    soup = BeautifulSoup(test_html_desc, "html.parser")
    desc = scraper._extract_description(soup)

    if "detailed description" in desc:
        print("✓ PASSED: Description extracted from HTML")
        tests_passed += 1
    else:
        print(f"✗ FAILED: Description extraction (got '{desc}')")
        tests_failed += 1

    print()

    # Test 5: Image extraction
    print("Test 5: Image Extraction")
    print("-" * 40)
    test_html_images = """
    <html>
    <body>
        <div class="product-images">
            <img class="product-image" src="/images/product1.jpg" />
            <img class="product-image" src="/images/product2.jpg" />
        </div>
    </body>
    </html>
    """

    soup = BeautifulSoup(test_html_images, "html.parser")
    images = scraper._extract_images(soup, "https://example.com")

    if len(images) >= 2 and "example.com" in images[0]:
        print(f"✓ PASSED: Extracted {len(images)} images with absolute URLs")
        tests_passed += 1
    else:
        print(f"✗ FAILED: Image extraction (got {len(images)} images)")
        tests_failed += 1

    print()

    # Test 6: Availability extraction
    print("Test 6: Availability Extraction")
    print("-" * 40)
    test_html_avail = """
    <html>
    <body>
        <span class="stock-status">In Stock</span>
    </body>
    </html>
    """

    soup = BeautifulSoup(test_html_avail, "html.parser")
    avail = scraper._extract_availability(soup)

    if "Stock" in avail:
        print("✓ PASSED: Availability status extracted")
        tests_passed += 1
    else:
        print(f"✗ FAILED: Availability extraction (got '{avail}')")
        tests_failed += 1

    print()

    # Summary
    print("=" * 80)
    print("TEST RESULTS")
    print("=" * 80)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print()

    if tests_failed == 0:
        print("✓ ALL TESTS PASSED - Scraper is working correctly!")
        print("The scraper is ready to use in your workflow.")
    else:
        print("⚠ SOME TESTS FAILED - Please check the implementation.")

    print("=" * 80)
    print()

    return tests_failed == 0


# ============================================================================
# EXAMPLE USAGE
# ============================================================================


def example_usage():
    """Show example usage of the scraper."""
    print("=" * 80)
    print("EXAMPLE USAGE")
    print("=" * 80)
    print()

    print("Example 1: Basic scraping")
    print("-" * 40)
    print("""
scraper = EcommerceProductScraper()
result = scraper.scrape("https://example.com/product/123")

print(f"Product: {result['name']}")
print(f"Price: {result['currency']} {result['price']}")
print(f"Description: {result['description'][:100]}...")
print(f"Images: {len(result['images'])} found")
print(f"Status: {result['availability']}")
""")
    print()

    print("Example 2: Custom configuration")
    print("-" * 40)
    print("""
scraper = EcommerceProductScraper(
    timeout=60,        # Longer timeout
    max_images=10      # Get more images
)
result = scraper.scrape("https://store.com/product")
""")
    print()

    print("Example 3: Batch scraping")
    print("-" * 40)
    print("""
scraper = EcommerceProductScraper()
urls = [
    "https://example.com/product/1",
    "https://example.com/product/2",
    "https://example.com/product/3"
]

for url in urls:
    result = scraper.scrape(url)
    if not result['error']:
        print(f"Scraped: {result['name']}")
""")
    print()

    print("Example 4: Error handling")
    print("-" * 40)
    print("""
scraper = EcommerceProductScraper()
result = scraper.scrape("https://example.com/product/123")

if result['error']:
    print(f"Error: {result['error']}")
else:
    print(f"Success: {result['name']}")
""")
    print()

    print("=" * 80)
    print()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main():
    """Main entry point - run tests and show examples."""
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "E-COMMERCE PRODUCT SCRAPER - COMPLETE VERSION" + " " * 16 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    print("This scraper extracts product information from e-commerce websites.")
    print("NO EXTERNAL APIs REQUIRED - only scrapes public HTML pages.")
    print()

    # Run built-in tests
    tests_passed = run_tests()

    # Show example usage
    example_usage()

    # Final instructions
    print("=" * 80)
    print("READY TO USE")
    print("=" * 80)
    print()
    print("To use this scraper in your workflow:")
    print("1. Copy this entire file to your project")
    print("2. Install dependencies: pip install requests beautifulsoup4")
    print("3. Import and use:")
    print()
    print("   from ecommerce_scraper_complete import EcommerceProductScraper")
    print("   scraper = EcommerceProductScraper()")
    print("   result = scraper.scrape('YOUR_PRODUCT_URL_HERE')")
    print()
    print("=" * 80)
    print()

    return 0 if tests_passed else 1


if __name__ == "__main__":
    sys.exit(main())
