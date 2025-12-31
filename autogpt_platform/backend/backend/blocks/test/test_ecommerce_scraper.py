"""Tests for the E-commerce Product Scraper Block."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.blocks.ecommerce_scraper import EcommerceProductScraperBlock
from backend.util.request import Response


class TestEcommerceProductScraperBlock:
    """Test suite for E-commerce Product Scraper Block."""

    @pytest.fixture
    def scraper_block(self):
        """Create a scraper block instance."""
        return EcommerceProductScraperBlock()

    @pytest.fixture
    def sample_html_with_json_ld(self):
        """Sample HTML with JSON-LD structured data."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org/",
                "@type": "Product",
                "name": "Test Product",
                "description": "A sample test product",
                "image": "https://example.com/image.jpg",
                "offers": {
                    "@type": "Offer",
                    "price": "99.99",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock"
                }
            }
            </script>
        </head>
        <body>
            <h1>Test Product</h1>
            <div class="price">$99.99</div>
            <div class="description">A sample test product</div>
        </body>
        </html>
        """

    @pytest.fixture
    def sample_html_without_json_ld(self):
        """Sample HTML without JSON-LD structured data."""
        return """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Basic Product</h1>
            <div class="price-main">$49.99</div>
            <div class="product-description">Basic product description</div>
            <img class="product-image" src="https://example.com/basic.jpg" alt="Product"/>
            <span class="stock-status">In Stock</span>
        </body>
        </html>
        """

    @pytest.fixture
    def mock_response_json_ld(self, sample_html_with_json_ld):
        """Mock a successful HTTP response with JSON-LD."""
        response = MagicMock(spec=Response)
        response.status = 200
        response.text.return_value = sample_html_with_json_ld
        return response

    @pytest.fixture
    def mock_response_no_json_ld(self, sample_html_without_json_ld):
        """Mock a successful HTTP response without JSON-LD."""
        response = MagicMock(spec=Response)
        response.status = 200
        response.text.return_value = sample_html_without_json_ld
        return response

    @pytest.mark.asyncio
    @patch("backend.blocks.ecommerce_scraper.Requests")
    async def test_scraper_with_json_ld(
        self,
        mock_requests_class,
        scraper_block,
        mock_response_json_ld,
    ):
        """Test scraping with JSON-LD structured data."""
        # Setup mock
        mock_requests = MagicMock()
        mock_requests.request = AsyncMock(return_value=mock_response_json_ld)
        mock_requests_class.return_value = mock_requests

        # Create input
        input_data = scraper_block.Input(
            url="https://example.com/product/123",
            extract_json_ld=True,
        )

        # Execute block
        outputs = {}
        async for output_name, output_data in scraper_block.run(
            input_data,
            graph_exec_id="test-exec-id",
            user_id="test-user",
        ):
            outputs[output_name] = output_data

        # Verify results
        assert "name" in outputs
        assert outputs["name"] == "Test Product"
        assert "price" in outputs
        assert outputs["price"] == "99.99"
        assert "description" in outputs
        assert outputs["description"] == "A sample test product"
        assert "currency" in outputs
        assert outputs["currency"] == "USD"
        assert "images" in outputs
        assert "https://example.com/image.jpg" in outputs["images"]
        assert "url" in outputs
        assert outputs["url"] == "https://example.com/product/123"

    @pytest.mark.asyncio
    @patch("backend.blocks.ecommerce_scraper.Requests")
    async def test_scraper_without_json_ld(
        self,
        mock_requests_class,
        scraper_block,
        mock_response_no_json_ld,
    ):
        """Test scraping with CSS selectors when JSON-LD is not available."""
        # Setup mock
        mock_requests = MagicMock()
        mock_requests.request = AsyncMock(return_value=mock_response_no_json_ld)
        mock_requests_class.return_value = mock_requests

        # Create input
        input_data = scraper_block.Input(
            url="https://example.com/product/456",
            extract_json_ld=False,
            name_selector="h1",
            price_selector='[class*="price"]',
            description_selector='[class*="description"]',
        )

        # Execute block
        outputs = {}
        async for output_name, output_data in scraper_block.run(
            input_data,
            graph_exec_id="test-exec-id",
            user_id="test-user",
        ):
            outputs[output_name] = output_data

        # Verify results
        assert "name" in outputs
        assert outputs["name"] == "Basic Product"
        assert "raw_html" in outputs
        assert "url" in outputs
        assert outputs["url"] == "https://example.com/product/456"

    @pytest.mark.asyncio
    @patch("backend.blocks.ecommerce_scraper.Requests")
    async def test_scraper_http_error(
        self,
        mock_requests_class,
        scraper_block,
    ):
        """Test scraper handling of HTTP errors."""
        # Setup mock for 404 error
        mock_response = MagicMock(spec=Response)
        mock_response.status = 404

        mock_requests = MagicMock()
        mock_requests.request = AsyncMock(return_value=mock_response)
        mock_requests_class.return_value = mock_requests

        # Create input
        input_data = scraper_block.Input(
            url="https://example.com/product/nonexistent",
        )

        # Execute block
        outputs = {}
        async for output_name, output_data in scraper_block.run(
            input_data,
            graph_exec_id="test-exec-id",
            user_id="test-user",
        ):
            outputs[output_name] = output_data

        # Verify error handling
        assert "error" in outputs
        assert "404" in outputs["error"]

    def test_extract_json_ld(self, scraper_block, sample_html_with_json_ld):
        """Test JSON-LD extraction from HTML."""
        json_ld = scraper_block._extract_json_ld(sample_html_with_json_ld)

        assert json_ld is not None
        assert json_ld.get("@type") == "Product"
        assert json_ld.get("name") == "Test Product"
        assert "offers" in json_ld
        assert json_ld["offers"]["price"] == "99.99"

    def test_extract_price_details(self, scraper_block):
        """Test price and currency extraction."""
        # Test USD
        price, currency = scraper_block._extract_price_details("$99.99")
        assert price == "99.99"
        assert currency == "USD"

        # Test EUR
        price, currency = scraper_block._extract_price_details("€49.50")
        assert price == "49.50"
        assert currency == "EUR"

        # Test GBP
        price, currency = scraper_block._extract_price_details("£29.99")
        assert price == "29.99"
        assert currency == "GBP"

        # Test with comma separator
        price, currency = scraper_block._extract_price_details("$1,299.99")
        assert price == "1,299.99"
        assert currency == "USD"

    def test_extract_with_css_h1(self, scraper_block):
        """Test CSS extraction for h1 tags."""
        html = "<h1>Product Title</h1>"
        result = scraper_block._extract_with_css(html, "h1")
        assert result == "Product Title"

    def test_extract_with_css_class(self, scraper_block):
        """Test CSS extraction for class selectors."""
        html = '<div class="product-price">$99.99</div>'
        result = scraper_block._extract_with_css(html, '[class*="price"]')
        assert result == "$99.99"
