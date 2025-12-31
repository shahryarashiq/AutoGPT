"""
E-commerce Product Scraper - Standalone Version

A complete, self-contained Python script for scraping product details from e-commerce websites.
This version can be loaded directly into your workspace without dependencies on the AutoGPT platform.

Features:
- Extracts product name, price, description, images, and availability
- Supports JSON-LD structured data extraction (schema.org Product markup)
- Falls back to configurable CSS selectors for flexible site support
- Smart currency detection (USD, EUR, GBP, JPY, INR)
- Handles various HTML formats and quote styles

Usage:
    python ecommerce_product_scraper_standalone.py <product_url>

Or import as a module:
    from ecommerce_product_scraper_standalone import EcommerceProductScraper
    
    scraper = EcommerceProductScraper()
    result = scraper.scrape("https://example.com/product/123")
    print(result)
"""

import asyncio
import json
import logging
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import aiohttp
except ImportError:
    print("Error: aiohttp is required. Install it with: pip install aiohttp")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EcommerceProductScraper:
    """
    A standalone scraper for extracting product information from e-commerce websites.
    """

    def __init__(
        self,
        name_selector: str = "h1",
        price_selector: str = '[class*="price"]',
        description_selector: str = '[class*="description"]',
        image_selector: str = 'img[class*="product"]',
        availability_selector: str = '[class*="availability"], [class*="stock"]',
        extract_json_ld: bool = True,
        max_images: int = 5,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        timeout: int = 30,
    ):
        """
        Initialize the scraper with configurable parameters.

        Args:
            name_selector: CSS selector for product name (default: "h1")
            price_selector: CSS selector for product price (default: '[class*="price"]')
            description_selector: CSS selector for description (default: '[class*="description"]')
            image_selector: CSS selector for images (default: 'img[class*="product"]')
            availability_selector: CSS selector for availability (default: '[class*="availability"], [class*="stock"]')
            extract_json_ld: Whether to extract JSON-LD data (default: True)
            max_images: Maximum number of images to extract (default: 5)
            user_agent: User agent string for requests (default: Chrome on Windows)
            timeout: Request timeout in seconds (default: 30)
        """
        self.name_selector = name_selector
        self.price_selector = price_selector
        self.description_selector = description_selector
        self.image_selector = image_selector
        self.availability_selector = availability_selector
        self.extract_json_ld = extract_json_ld
        self.max_images = max_images
        self.user_agent = user_agent
        self.timeout = timeout

    @staticmethod
    def _extract_with_css(html: str, selector: str) -> str:
        """
        Extract text from HTML using a CSS selector pattern.

        This is a lightweight regex-based implementation for common patterns.
        It supports basic CSS selectors like:
        - Tag selectors (e.g., "h1")
        - Class attribute selectors (e.g., '[class*="price"]')
        - Image src extraction (e.g., 'img[class*="product"]')

        Limitations:
        - Does not support complex CSS selector syntax
        - May not handle all edge cases in HTML structure
        - Works best with well-formed HTML
        """
        pattern = None

        if selector.startswith('[class*="'):
            # Extract class pattern
            class_pattern = selector.split('"')[1]
            pattern = rf'class="[^"]*{re.escape(class_pattern)}[^"]*"[^>]*>([^<]+)'
        elif selector.startswith("h1"):
            pattern = r"<h1[^>]*>([^<]+)</h1>"
        elif selector.startswith("img"):
            # For images, extract src attribute (handles single quotes, double quotes, or no quotes)
            if 'class*="' in selector:
                class_pattern = selector.split('"')[1]
                pattern = rf'<img[^>]*class=["\']?[^"\']*{re.escape(class_pattern)}[^"\']*["\']?[^>]*src=["\']?([^"\'\s>]+)["\']?'
            else:
                pattern = r'<img[^>]*src=["\']?([^"\'\s>]+)["\']?'
        else:
            # Generic tag extraction
            tag = selector.strip()
            pattern = rf"<{tag}[^>]*>([^<]+)</{tag}>"

        if pattern:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()

        return ""

    @staticmethod
    def _extract_json_ld(html: str) -> Dict[str, Any]:
        """Extract structured data from JSON-LD script tags."""
        # Look for JSON-LD script tags
        pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

        for match in matches:
            try:
                data = json.loads(match.strip())
                # Look for Product schema
                if isinstance(data, dict):
                    if data.get("@type") == "Product":
                        return data
                    # Check if it's a graph with Product
                    if "@graph" in data:
                        for item in data["@graph"]:
                            if (
                                isinstance(item, dict)
                                and item.get("@type") == "Product"
                            ):
                                return item
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Product":
                            return item
            except json.JSONDecodeError:
                continue

        return {}

    @staticmethod
    def _extract_price_details(price_text: str) -> Tuple[str, str]:
        """
        Extract currency and numeric price from price text.

        Handles common formats:
        - US format: 1,234.56 or 1234.56
        - European format: 1.234,56 or 1234,56

        Note: Ambiguous formats (e.g., "1.234") are treated as US format.
        """
        # Common currency symbols and codes
        currency_patterns = {
            r"$": "USD",
            r"€": "EUR",
            r"£": "GBP",
            r"¥": "JPY",
            r"₹": "INR",
            r"USD": "USD",
            r"EUR": "EUR",
            r"GBP": "GBP",
        }

        currency = ""
        for pattern, code in currency_patterns.items():
            if pattern in price_text:
                currency = code
                break

        # Extract numeric price - handles both US and European formats
        # US: 1,234.56  EU: 1.234,56
        price_match = re.search(r"\d{1,3}(?:[,.]\d{3})*[.,]?\d{0,2}", price_text)
        if price_match:
            price = price_match.group(0)
            # Validate that we have a reasonable price format
            if not re.search(r"[.,]\d$", price):  # Ends with single digit after separator
                return price, currency
            return price, currency

        return price_text, currency

    async def _fetch_page(self, url: str) -> str:
        """Fetch the HTML content of a page."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch page: HTTP {response.status}")
                return await response.text()

    async def scrape_async(self, url: str) -> Dict[str, Any]:
        """
        Scrape product information from a URL (async version).

        Args:
            url: The product page URL to scrape

        Returns:
            Dictionary containing extracted product information:
            - name: Product name
            - price: Product price (numeric value as string)
            - description: Product description
            - images: List of product image URLs
            - availability: Product availability status
            - currency: Price currency code
            - raw_html: Complete HTML content
            - json_ld_data: Structured data from JSON-LD if available
            - url: The scraped URL
            - error: Error message if scraping failed
        """
        result: Dict[str, Any] = {
            "url": url,
            "name": "",
            "price": "",
            "description": "",
            "images": [],
            "availability": "",
            "currency": "",
            "raw_html": "",
            "json_ld_data": {},
            "error": "",
        }

        try:
            # Fetch the page
            html_content = await self._fetch_page(url)
            result["raw_html"] = html_content

            # Extract JSON-LD structured data if requested
            if self.extract_json_ld:
                json_ld_data = self._extract_json_ld(html_content)
                if json_ld_data:
                    result["json_ld_data"] = json_ld_data

                    # Use JSON-LD data if available
                    if "name" in json_ld_data:
                        result["name"] = json_ld_data["name"]
                    if "description" in json_ld_data:
                        result["description"] = json_ld_data["description"]
                    if "offers" in json_ld_data:
                        offers = json_ld_data["offers"]
                        if isinstance(offers, dict):
                            if "price" in offers:
                                result["price"] = str(offers["price"])
                            if "priceCurrency" in offers:
                                result["currency"] = offers["priceCurrency"]
                            if "availability" in offers:
                                result["availability"] = offers["availability"]
                    if "image" in json_ld_data:
                        images = json_ld_data["image"]
                        if isinstance(images, str):
                            result["images"] = [images]
                        elif isinstance(images, list):
                            result["images"] = images

                    # If we got everything from JSON-LD, we're done
                    if all(key in json_ld_data for key in ["name", "offers"]):
                        return result

            # Fall back to CSS selector extraction
            if not result["name"]:
                name = self._extract_with_css(html_content, self.name_selector)
                if name:
                    result["name"] = name

            if not result["price"]:
                price_text = self._extract_with_css(html_content, self.price_selector)
                if price_text:
                    price, currency = self._extract_price_details(price_text)
                    result["price"] = price
                    if currency and not result["currency"]:
                        result["currency"] = currency

            if not result["description"]:
                description = self._extract_with_css(
                    html_content, self.description_selector
                )
                if description:
                    result["description"] = description

            # Extract images if not already extracted from JSON-LD
            if not result["images"]:
                image_pattern = (
                    rf'{self.image_selector}[^>]*src=["\']?([^"\'\s>]+)["\']?'
                )
                image_matches = re.findall(
                    image_pattern, html_content, re.IGNORECASE
                )
                if image_matches:
                    result["images"] = image_matches[: self.max_images]

            if not result["availability"]:
                availability = self._extract_with_css(
                    html_content, self.availability_selector
                )
                if availability:
                    result["availability"] = availability

        except Exception as e:
            logger.exception(f"Error scraping product from {url}")
            result["error"] = f"Scraping error: {str(e)}"

        return result

    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape product information from a URL (synchronous version).

        Args:
            url: The product page URL to scrape

        Returns:
            Dictionary containing extracted product information
        """
        return asyncio.run(self.scrape_async(url))


def format_output(result: Dict[str, Any], include_html: bool = False) -> str:
    """Format the scraping result for display."""
    lines = [
        "=" * 80,
        "PRODUCT INFORMATION",
        "=" * 80,
        f"URL: {result['url']}",
        "",
    ]

    if result["error"]:
        lines.append(f"ERROR: {result['error']}")
        lines.append("")
    else:
        if result["name"]:
            lines.append(f"Name: {result['name']}")
        if result["price"]:
            price_display = (
                f"{result['currency']} {result['price']}"
                if result["currency"]
                else result["price"]
            )
            lines.append(f"Price: {price_display}")
        if result["availability"]:
            lines.append(f"Availability: {result['availability']}")
        if result["description"]:
            desc = (
                result["description"][:200] + "..."
                if len(result["description"]) > 200
                else result["description"]
            )
            lines.append(f"Description: {desc}")
        if result["images"]:
            lines.append(f"Images ({len(result['images'])}):")
            for i, img in enumerate(result["images"][:5], 1):
                lines.append(f"  {i}. {img}")
        if result["json_ld_data"]:
            lines.append(f"JSON-LD Data: Available (schema.org Product)")

    if include_html and result["raw_html"]:
        lines.append("")
        lines.append("RAW HTML (first 500 chars):")
        lines.append(result["raw_html"][:500] + "...")

    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    """Command-line interface for the scraper."""
    if len(sys.argv) < 2:
        print("Usage: python ecommerce_product_scraper_standalone.py <product_url>")
        print("\nExample:")
        print("  python ecommerce_product_scraper_standalone.py https://example.com/product/123")
        sys.exit(1)

    url = sys.argv[1]
    include_html = "--include-html" in sys.argv

    print(f"Scraping product from: {url}")
    print("Please wait...\n")

    scraper = EcommerceProductScraper()
    result = scraper.scrape(url)

    print(format_output(result, include_html=include_html))

    # Also save as JSON
    output_file = "product_data.json"
    # Don't include raw_html in JSON output unless requested
    json_result = {k: v for k, v in result.items() if k != "raw_html" or include_html}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_result, f, indent=2, ensure_ascii=False)
    print(f"\nFull data saved to: {output_file}")


if __name__ == "__main__":
    main()
