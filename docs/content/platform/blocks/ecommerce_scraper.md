# E-commerce Product Scraper

## What it is
The E-commerce Product Scraper block is a tool for extracting structured product information from e-commerce websites.

## What it does
This block fetches product pages from e-commerce websites and extracts key product details such as name, price, description, images, and availability status. It intelligently uses JSON-LD structured data when available, and falls back to CSS selectors for flexible extraction from various e-commerce platforms.

## How it works
When activated, the block sends an HTTP request to the specified product URL. It first attempts to extract product information from JSON-LD structured data (schema.org Product markup) which many modern e-commerce sites include. If JSON-LD data is not available or incomplete, it falls back to using configurable CSS selectors to extract information from the HTML content. The block also includes smart parsing for prices and currency symbols.

## Inputs
| Input | Description |
|-------|-------------|
| URL | The web address of the product page to scrape (e.g., https://example.com/product/item-123) |
| Name Selector | CSS selector or regex pattern to extract product name. Default is "h1" |
| Price Selector | CSS selector or regex pattern to extract product price. Default is '[class*="price"]' |
| Description Selector | CSS selector or regex pattern to extract product description. Default is '[class*="description"]' |
| Image Selector | CSS selector to extract product image URLs. Default is 'img[class*="product"]' |
| Availability Selector | CSS selector or regex pattern to extract availability status. Default is '[class*="availability"], [class*="stock"]' |
| Extract JSON-LD | Whether to extract structured data from JSON-LD schema if available. Default is True |
| User Agent | User agent string to use for the request. Default is a standard browser user agent |
| Timeout | Request timeout in seconds. Default is 30 |

## Outputs
| Output | Description |
|--------|-------------|
| Name | The product name |
| Price | The product price (numeric value) |
| Description | The product description text |
| Images | List of product image URLs |
| Availability | Product availability status (e.g., "In Stock", "Out of Stock") |
| Currency | Price currency code (e.g., "USD", "EUR", "GBP") |
| Raw HTML | Complete HTML content of the product page |
| JSON-LD Data | Structured data from JSON-LD if available |
| URL | The scraped product URL |
| Error | Error message if scraping failed |

## Possible use cases

### Price Monitoring
Monitor product prices across multiple e-commerce sites to track price changes, find the best deals, or trigger alerts when prices drop below a certain threshold.

### Product Research
Gather product information from various e-commerce platforms for market research, competitive analysis, or creating product catalogs.

### Inventory Management
Track product availability across different online stores to manage inventory, identify out-of-stock items, or monitor competitor stock levels.

### Data Aggregation
Aggregate product data from multiple sources to build comparison shopping tools, price comparison websites, or product recommendation systems.

## Technical Details

### JSON-LD Support
The block automatically detects and parses JSON-LD structured data following the schema.org Product specification. This provides the most reliable extraction method for sites that include this markup.

### CSS Selector Fallback
When JSON-LD is not available, the block uses CSS selectors to extract information. The default selectors are designed to work with common e-commerce site structures, but can be customized for specific websites.

### Currency Detection
The block automatically detects and extracts currency information from price text, supporting common currency symbols ($, €, £, ¥, ₹) and ISO currency codes.

## Example Usage

### Basic Product Scraping
1. Set the URL input to the product page you want to scrape
2. Leave other inputs at their defaults
3. Run the block
4. Access the extracted product information from the output pins

### Custom Selector Configuration
For sites with unique HTML structures:
1. Inspect the product page HTML to identify the appropriate selectors
2. Configure the selector inputs to match the site's structure
3. Disable JSON-LD extraction if the site doesn't use it
4. Run the block to extract product information

### Integration with Other Blocks
The scraper can be combined with other blocks for powerful workflows:
- Use with the **Send Web Request** block to handle authentication or session cookies
- Connect to **Spreadsheet** blocks to store extracted data
- Use with **Branching** blocks to handle different product types
- Combine with **Text** blocks to format and clean extracted data
