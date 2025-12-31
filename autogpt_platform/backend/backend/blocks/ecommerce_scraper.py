"""
E-commerce Product Scraper Block

This block scrapes product details from e-commerce websites, extracting structured
information such as product name, price, description, images, and availability.
"""

import logging
import re
from enum import Enum
from typing import Any

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField
from backend.util.request import Requests

logger = logging.getLogger(__name__)


class SelectorType(Enum):
    """Type of CSS selector or extraction pattern to use"""

    CSS = "css"
    REGEX = "regex"
    JSON_LD = "json_ld"


class EcommerceProductScraperBlock(Block):
    """
    Scrapes product details from e-commerce websites.

    This block fetches a product page and extracts structured information
    using configurable selectors. It supports:
    - CSS selectors for HTML element extraction
    - Regular expression patterns
    - JSON-LD structured data extraction
    """

    class Input(BlockSchema):
        url: str = SchemaField(
            description="The URL of the product page to scrape",
            placeholder="https://example.com/product/item-123",
        )
        name_selector: str = SchemaField(
            description="CSS selector or regex pattern to extract product name",
            default="h1",
        )
        price_selector: str = SchemaField(
            description="CSS selector or regex pattern to extract product price",
            default='[class*="price"]',
        )
        description_selector: str = SchemaField(
            description="CSS selector or regex pattern to extract product description",
            default='[class*="description"]',
        )
        image_selector: str = SchemaField(
            description="CSS selector to extract product image URL",
            default='img[class*="product"]',
        )
        availability_selector: str = SchemaField(
            description="CSS selector or regex pattern to extract availability status",
            default='[class*="availability"], [class*="stock"]',
        )
        extract_json_ld: bool = SchemaField(
            description="Extract structured data from JSON-LD schema if available",
            default=True,
        )
        user_agent: str = SchemaField(
            description="User agent string to use for the request",
            default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )
        timeout: int = SchemaField(
            description="Request timeout in seconds",
            default=30,
        )

    class Output(BlockSchema):
        name: str = SchemaField(description="Product name")
        price: str = SchemaField(description="Product price")
        description: str = SchemaField(description="Product description")
        images: list[str] = SchemaField(description="Product image URLs")
        availability: str = SchemaField(description="Product availability status")
        currency: str = SchemaField(description="Price currency")
        raw_html: str = SchemaField(description="Raw HTML content of the page")
        json_ld_data: dict[str, Any] = SchemaField(
            description="Structured data from JSON-LD if available"
        )
        url: str = SchemaField(description="The scraped product URL")
        error: str = SchemaField(description="Error message if scraping failed")

    def __init__(self):
        super().__init__(
            id="a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
            description="Scrapes product details from e-commerce websites including name, price, description, images, and availability.",
            categories={BlockCategory.SEARCH, BlockCategory.INPUT},
            input_schema=EcommerceProductScraperBlock.Input,
            output_schema=EcommerceProductScraperBlock.Output,
        )

    @staticmethod
    def _extract_with_css(html: str, selector: str) -> str:
        """
        Extract text from HTML using a CSS selector pattern.
        This is a simple implementation that looks for common patterns.
        """
        # Simple CSS selector matching for common cases
        # For production use, consider using a proper HTML parser library
        pattern = None

        if selector.startswith('[class*="'):
            # Extract class pattern
            class_pattern = selector.split('"')[1]
            pattern = rf'class="[^"]*{re.escape(class_pattern)}[^"]*"[^>]*>([^<]+)'
        elif selector.startswith("h1"):
            pattern = r"<h1[^>]*>([^<]+)</h1>"
        elif selector.startswith("img"):
            # For images, extract src attribute
            if 'class*="' in selector:
                class_pattern = selector.split('"')[1]
                pattern = rf'<img[^>]*class="[^"]*{re.escape(class_pattern)}[^"]*"[^>]*src="([^"]+)"'
            else:
                pattern = r'<img[^>]*src="([^"]+)"'
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
    def _extract_json_ld(html: str) -> dict[str, Any]:
        """Extract structured data from JSON-LD script tags."""
        import json

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
    def _extract_price_details(price_text: str) -> tuple[str, str]:
        """Extract currency and numeric price from price text."""
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

        # Extract numeric price
        price_match = re.search(r"[\d,]+\.?\d*", price_text)
        if price_match:
            return price_match.group(0), currency

        return price_text, currency

    async def run(self, input_data: Input, **kwargs) -> BlockOutput:
        try:
            # Make the HTTP request
            headers = {
                "User-Agent": input_data.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }

            response = await Requests().request(
                "GET",
                input_data.url,
                headers=headers,
                timeout=input_data.timeout,
            )

            if response.status != 200:
                yield "error", f"Failed to fetch page: HTTP {response.status}"
                return

            html_content = response.text()
            yield "raw_html", html_content
            yield "url", input_data.url

            # Extract JSON-LD structured data if requested
            json_ld_data = {}
            if input_data.extract_json_ld:
                json_ld_data = self._extract_json_ld(html_content)
                if json_ld_data:
                    yield "json_ld_data", json_ld_data

                    # Use JSON-LD data if available
                    if "name" in json_ld_data:
                        yield "name", json_ld_data["name"]
                    if "description" in json_ld_data:
                        yield "description", json_ld_data["description"]
                    if "offers" in json_ld_data:
                        offers = json_ld_data["offers"]
                        if isinstance(offers, dict):
                            if "price" in offers:
                                yield "price", str(offers["price"])
                            if "priceCurrency" in offers:
                                yield "currency", offers["priceCurrency"]
                            if "availability" in offers:
                                yield "availability", offers["availability"]
                    if "image" in json_ld_data:
                        images = json_ld_data["image"]
                        if isinstance(images, str):
                            yield "images", [images]
                        elif isinstance(images, list):
                            yield "images", images

                    # If we got everything from JSON-LD, we're done
                    if all(key in json_ld_data for key in ["name", "offers"]):
                        return

            # Fall back to CSS selector extraction
            name = self._extract_with_css(html_content, input_data.name_selector)
            if name:
                yield "name", name

            price_text = self._extract_with_css(html_content, input_data.price_selector)
            if price_text:
                price, currency = self._extract_price_details(price_text)
                yield "price", price
                if currency:
                    yield "currency", currency

            description = self._extract_with_css(
                html_content, input_data.description_selector
            )
            if description:
                yield "description", description

            # Extract images
            image_urls = []
            image_pattern = rf'{input_data.image_selector}[^>]*src="([^"]+)"'
            image_matches = re.findall(image_pattern, html_content, re.IGNORECASE)
            if image_matches:
                image_urls = image_matches[:5]  # Limit to first 5 images
                yield "images", image_urls

            availability = self._extract_with_css(
                html_content, input_data.availability_selector
            )
            if availability:
                yield "availability", availability

        except Exception as e:
            logger.exception(f"Error scraping product from {input_data.url}")
            yield "error", f"Scraping error: {str(e)}"
