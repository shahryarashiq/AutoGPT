# E-commerce Product Scraper - Complete Standalone Package

This is a complete, self-contained e-commerce product scraper that you can use directly in your workspace. No AutoGPT platform dependencies required!

## Files Included

1. **ecommerce_product_scraper_standalone.py** - The complete scraper implementation
2. **README_STANDALONE.md** - This file with usage instructions

## Installation

### Requirements

Only one external dependency is needed:

```bash
pip install aiohttp
```

That's it! The scraper is ready to use.

## Quick Start

### Command-Line Usage

```bash
# Basic usage
python ecommerce_product_scraper_standalone.py https://example.com/product/123

# Include raw HTML in output
python ecommerce_product_scraper_standalone.py https://example.com/product/123 --include-html
```

### Python Script Usage

```python
from ecommerce_product_scraper_standalone import EcommerceProductScraper

# Create scraper instance with default settings
scraper = EcommerceProductScraper()

# Scrape a product page
result = scraper.scrape("https://example.com/product/123")

# Access the results
print(f"Product Name: {result['name']}")
print(f"Price: {result['currency']} {result['price']}")
print(f"Description: {result['description']}")
print(f"Images: {len(result['images'])} found")
print(f"Availability: {result['availability']}")
```

### Custom Configuration

```python
scraper = EcommerceProductScraper(
    name_selector="h1.product-title",           # Custom CSS selector for name
    price_selector='span[class*="price"]',      # Custom CSS selector for price
    description_selector='div.description',      # Custom CSS selector for description
    image_selector='img.product-image',         # Custom CSS selector for images
    extract_json_ld=True,                       # Enable JSON-LD extraction
    max_images=10,                              # Maximum images to extract
    timeout=60                                   # Request timeout in seconds
)

result = scraper.scrape("https://yoursite.com/product")
```

### Async Usage

```python
import asyncio
from ecommerce_product_scraper_standalone import EcommerceProductScraper

async def scrape_multiple():
    scraper = EcommerceProductScraper()
    
    urls = [
        "https://example.com/product/1",
        "https://example.com/product/2",
        "https://example.com/product/3"
    ]
    
    tasks = [scraper.scrape_async(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"Scraped: {result['name']} - {result['price']}")

# Run async scraping
asyncio.run(scrape_multiple())
```

## Features

### 1. JSON-LD Extraction (Recommended)

The scraper automatically detects and extracts product information from JSON-LD structured data (schema.org Product markup). This is the most reliable method and works with many modern e-commerce sites.

**Example websites that support JSON-LD:**
- Most Shopify stores
- WooCommerce sites with structured data plugins
- Major retailers (Amazon, eBay, etc.)

### 2. CSS Selector Fallback

When JSON-LD is not available, the scraper uses configurable CSS selectors to extract information from HTML. You can customize these selectors for specific websites.

### 3. Smart Price Parsing

Automatically detects and extracts:
- Currency symbols: $, €, £, ¥, ₹
- Currency codes: USD, EUR, GBP, JPY, INR
- Various number formats: 1,234.56 (US) or 1.234,56 (EU)

### 4. Flexible Image Extraction

Handles different HTML quote styles:
- Double quotes: `src="image.jpg"`
- Single quotes: `src='image.jpg'`
- No quotes: `src=image.jpg`

## Output Format

The scraper returns a dictionary with the following structure:

```python
{
    "url": "https://example.com/product/123",
    "name": "Product Name",
    "price": "99.99",
    "currency": "USD",
    "description": "Product description text...",
    "images": [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    "availability": "In Stock",
    "raw_html": "<html>...</html>",  # Full page HTML
    "json_ld_data": {                 # If JSON-LD found
        "@type": "Product",
        "name": "Product Name",
        "offers": {...}
    },
    "error": ""                       # Error message if scraping failed
}
```

## Advanced Examples

### Example 1: Batch Scraping with Error Handling

```python
from ecommerce_product_scraper_standalone import EcommerceProductScraper
import json

urls = [
    "https://example1.com/product/1",
    "https://example2.com/product/2",
    "https://example3.com/product/3"
]

scraper = EcommerceProductScraper(timeout=30)
results = []

for url in urls:
    try:
        result = scraper.scrape(url)
        if result["error"]:
            print(f"Error scraping {url}: {result['error']}")
        else:
            print(f"✓ Scraped: {result['name']}")
            results.append(result)
    except Exception as e:
        print(f"✗ Failed {url}: {e}")

# Save all results
with open("all_products.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Example 2: Price Monitoring

```python
from ecommerce_product_scraper_standalone import EcommerceProductScraper
import time

def monitor_price(url, target_price, check_interval=3600):
    """Monitor a product and alert when price drops below target."""
    scraper = EcommerceProductScraper()
    
    while True:
        result = scraper.scrape(url)
        
        if result["error"]:
            print(f"Error: {result['error']}")
        else:
            current_price = float(result["price"].replace(",", ""))
            print(f"{result['name']}: {result['currency']} {current_price}")
            
            if current_price <= target_price:
                print(f"🎉 ALERT! Price dropped to {current_price}!")
                break
        
        print(f"Checking again in {check_interval} seconds...")
        time.sleep(check_interval)

# Monitor a product
monitor_price("https://example.com/product/123", target_price=50.00)
```

### Example 3: Custom Selector for Specific Site

```python
from ecommerce_product_scraper_standalone import EcommerceProductScraper

# Configure scraper for a specific e-commerce platform
scraper = EcommerceProductScraper(
    name_selector="h1.product-name",
    price_selector="span.price-value",
    description_selector="div.product-details p",
    image_selector="img.product-photo",
    availability_selector="span.stock-status",
    extract_json_ld=False  # Disable if site doesn't use JSON-LD
)

result = scraper.scrape("https://specific-site.com/product")
print(f"Found: {result['name']} for {result['price']}")
```

### Example 4: Export to CSV

```python
from ecommerce_product_scraper_standalone import EcommerceProductScraper
import csv

urls = ["https://example.com/product/1", "https://example.com/product/2"]
scraper = EcommerceProductScraper()

# Scrape all products
products = [scraper.scrape(url) for url in urls]

# Export to CSV
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price", "currency", "availability", "url"])
    writer.writeheader()
    
    for product in products:
        if not product["error"]:
            writer.writerow({
                "name": product["name"],
                "price": product["price"],
                "currency": product["currency"],
                "availability": product["availability"],
                "url": product["url"]
            })

print("Products exported to products.csv")
```

## Troubleshooting

### Issue: No data extracted

**Solution:** The site might have custom HTML structure. Inspect the page source and update the CSS selectors:

```python
scraper = EcommerceProductScraper(
    name_selector="h1.custom-title",  # Update to match site's HTML
    price_selector="div.custom-price"
)
```

### Issue: Request timeout

**Solution:** Increase the timeout value:

```python
scraper = EcommerceProductScraper(timeout=60)  # 60 seconds
```

### Issue: Blocked by website

**Solution:** Some sites block scrapers. Try:
1. Using a different user agent
2. Adding delays between requests
3. Using the site's official API if available

```python
scraper = EcommerceProductScraper(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
)
```

### Issue: Invalid SSL certificate

**Solution:** For development only, you can modify the `_fetch_page` method to disable SSL verification (not recommended for production).

## Limitations

1. **Simple CSS Selector Support**: The built-in CSS selector parser supports basic patterns. For complex selectors, consider using BeautifulSoup or lxml.

2. **JavaScript-Rendered Content**: This scraper works with static HTML. For sites that load content with JavaScript, consider using Selenium or Playwright.

3. **Rate Limiting**: Be respectful of websites. Add delays between requests to avoid overwhelming servers.

4. **Legal Considerations**: Always check a website's robots.txt and terms of service before scraping.

## Best Practices

1. **Always check robots.txt** before scraping a website
2. **Add delays** between requests to avoid overloading servers
3. **Use JSON-LD** when available (most reliable)
4. **Handle errors gracefully** with try-except blocks
5. **Save results** periodically when scraping multiple pages
6. **Test selectors** on a few pages before batch scraping

## Integration with AutoGPT Platform

If you want to use this scraper as an AutoGPT block, the full implementation is available in:
- `/autogpt_platform/backend/backend/blocks/ecommerce_scraper.py`
- `/autogpt_platform/backend/backend/blocks/test/test_ecommerce_scraper.py`
- `/docs/content/platform/blocks/ecommerce_scraper.md`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in `ecommerce_product_scraper_standalone.py`
3. Consult the AutoGPT platform documentation for the block version

## License

This code is provided as-is for use within the AutoGPT project. Please respect the licenses of both the AutoGPT platform and any websites you scrape.
