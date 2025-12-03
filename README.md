# Umico Product Scraper & Market Analysis

Fast asynchronous scraper for Umico marketplace products with comprehensive market analysis and insights.

## Features

- **Blazing Fast**: Scrapes 11,000+ products in ~13 seconds using concurrent requests
- **Async/Await**: Built with asyncio and aiohttp for maximum performance
- **Error Handling**: Automatic retry logic with exponential backoff
- **CSV Export**: Clean, flattened data ready for analysis
- **Data Visualization**: 10 professional charts with market insights
- **Progress Tracking**: Real-time console updates during scraping

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Full Scrape

```bash
python3 umico_scraper.py
```

This will:
- Scrape all products from category 15
- Save to `umico_products.csv`
- Show progress for each page
- Complete in ~15 seconds

### Test Scrape

```bash
python3 test_scraper.py
```

Tests the scraper with only 3 pages to verify everything works.

### Generate Charts

```bash
python3 generate_charts.py
```

Generates 10 comprehensive market analysis charts in the `charts/` directory.

## Market Insights

Based on analysis of **11,712 products** from the Umico marketplace:

### 📊 Market Overview

- **Total Products Analyzed**: 11,712
- **Average Price**: 354.41 AZN
- **Median Price**: 69.00 AZN
- **Price Range**: 0.45 AZN - 23,281.65 AZN

### 💰 Pricing & Discounts

- **Products with Discounts**: 7,480 (63.9%)
- **Average Discount Rate**: 29.5%
- **Most Common Discount Range**: 20-30%
- **Maximum Discount Observed**: Up to 90%+

**Key Insight**: Nearly two-thirds of products offer discounts, with an average savings of 30%. This indicates aggressive competitive pricing in the marketplace.

### 🏆 Market Leaders

- **Top Brand**: HP (627 products)
- **Top Category**: Ofis avadanlığı üçün aksessuarlar (1,366 products)
- **Top Seller**: AllGoods Distributions (486 products)
- **Average Seller Rating**: 93.1/100

**Key Insight**: HP dominates the branded product space, while office accessories represent the largest category, indicating strong B2B/office supply demand.

### 💳 Payment Flexibility

- **Products with Installments**: 11,660 (99.6%)
- **Most Common Installment Period**: 18 months
- **Installment Range**: 3-30 months

**Key Insight**: Near-universal installment availability with flexible terms up to 30 months indicates a strong focus on purchase accessibility.

### 🏷️ Brand Analysis

**Top 5 Branded Products (excluding generic)**:
1. HP - 627 products (11.1%)
2. Canon - 434 products (7.7%)
3. Apple - 346 products (6.1%)
4. Lenovo - 300 products (5.3%)
5. Asus - 284 products (5.0%)

**Key Insight**: Technology brands dominate, with HP and Canon leading office and printing solutions market share.

### 📱 Category Distribution

**Top 5 Categories**:
1. Office Equipment Accessories - 1,366 products (11.7%)
2. Tablets - 995 products (8.5%)
3. Mouse Devices - 882 products (7.5%)
4. Power Strips & Extensions - 870 products (7.4%)
5. Laptops - 667 products (5.7%)

**Key Insight**: Strong focus on office/productivity accessories alongside core computing devices (tablets, laptops).

### 💵 Price Segmentation

**Product Distribution by Price**:
- **Budget (0-50 AZN)**: 5,462 products (46.6%)
- **Mid-Range (50-200 AZN)**: 3,689 products (31.5%)
- **Premium (200-1000 AZN)**: 2,056 products (17.6%)
- **Luxury (1000+ AZN)**: 505 products (4.3%)

**Key Insight**: Nearly half of all products are budget-friendly (under 50 AZN), indicating accessibility-focused market positioning.

### ⭐ Seller Quality

- **High-Rated Sellers (90-100)**: Majority of products
- **Average Seller Rating**: 93.1/100
- **Rating Distribution**: Strong concentration at 95-99 range

**Key Insight**: High seller ratings across the board indicate strong quality control and customer satisfaction standards.

---

## Data Visualizations

### 1. Top 15 Brands by Product Count

![Top Brands](charts/01_top_brands.png)

**Business Value**: Identifies market leaders and brand diversity. HP, Canon, and Apple dominate the marketplace, indicating strong consumer preference for established tech brands.

---

### 2. Price Distribution by Top Categories

![Price by Category](charts/02_price_by_category.png)

**Business Value**: Shows pricing strategies across categories. Wide price ranges in laptops vs. accessories indicate different market segments and profit margins.

---

### 3. Discount Distribution Analysis

![Discount Distribution](charts/03_discount_distribution.png)

**Business Value**: Reveals competitive pricing strategies. The concentration of 20-40% discounts suggests strategic promotional pricing rather than clearance sales.

---

### 4. Top 15 Sellers by Product Count

![Top Sellers](charts/04_top_sellers.png)

**Business Value**: Identifies key marketplace partners. AllGoods Distributions and MOON Mobil Aksesusar lead in product variety, indicating major distribution partnerships.

---

### 5. Product Distribution by Price Range

![Price Ranges](charts/05_price_ranges.png)

**Business Value**: Market segmentation analysis. The heavy concentration in 0-50 AZN range indicates a mass-market focus with accessibility as a priority.

---

### 6. Seller Rating Distribution

![Seller Ratings](charts/06_seller_ratings.png)

**Business Value**: Quality assurance metrics. High concentration of 95+ ratings demonstrates marketplace quality standards and customer satisfaction.

---

### 7. Installment Options Analysis

![Installment Options](charts/07_installment_options.png)

**Business Value**: Payment flexibility trends. 18-month installments dominate, balancing affordability with reasonable payback periods.

---

### 8. Product Rating vs Price Analysis

![Rating vs Price](charts/08_rating_vs_price.png)

**Business Value**: Quality-price correlation. Highly-rated products exist across all price points, indicating that quality isn't solely determined by price.

---

### 9. Top 15 Product Categories

![Top Categories](charts/09_top_categories.png)

**Business Value**: Category performance metrics. Office accessories and peripherals outperform core computing devices, suggesting strong recurring revenue from accessories market.

---

### 10. Brand Market Share (Top 10)

![Brand Market Share](charts/10_brand_market_share.png)

**Business Value**: Competitive landscape analysis. HP's 11% market share among branded products shows market fragmentation with opportunities for brand partnerships.

---

## Configuration

Edit these variables in `umico_scraper.py`:

```python
CATEGORY_ID = 15  # Change to scrape different category
PER_PAGE = 24     # Products per page
MAX_CONCURRENT_REQUESTS = 10  # Concurrent requests
OUTPUT_FILE = "umico_products.csv"  # Output filename
```

## Output Format

The CSV contains **29 columns** including:

| Column | Description |
|--------|-------------|
| `product_id` | Unique product identifier |
| `name` | Product name |
| `brand` | Brand name |
| `category_name` | Product category |
| `retail_price` | Current selling price |
| `old_price` | Original price (before discount) |
| `discount_percent` | Discount percentage |
| `seller_name` | Seller/vendor name |
| `seller_rating` | Seller rating (0-100) |
| `rating_value` | Product rating (0-5) |
| `rating_count` | Number of reviews |
| `installment_enabled` | Installment availability |
| `max_installment_months` | Maximum installment period |
| `image_small/medium/big` | Product image URLs |
| And 15+ more fields... | Full product metadata |

## Performance

- **Total Products**: 11,736
- **Total Pages**: 489
- **Scraping Time**: ~13 seconds
- **Speed**: ~900 products/second
- **Success Rate**: 100%
- **Chart Generation**: ~5 seconds

## Business Applications

This data and analysis can be used for:

1. **Competitive Intelligence**: Monitor competitor pricing and product strategies
2. **Market Research**: Identify trending categories and brands
3. **Pricing Strategy**: Benchmark pricing against market averages
4. **Inventory Planning**: Understand product diversity and category distribution
5. **Seller Analysis**: Evaluate seller performance and ratings
6. **Consumer Insights**: Analyze price sensitivity and discount patterns
7. **Partnership Opportunities**: Identify top-performing brands and sellers

## Requirements

- Python 3.7+
- aiohttp 3.9.1+
- pandas 1.5.0+
- matplotlib 3.5.0+
- seaborn 0.12.0+

## Project Structure

```
.
├── umico_scraper.py          # Main scraper script
├── test_scraper.py           # Test/validation script
├── generate_charts.py        # Chart generation script
├── umico_products.csv        # Scraped data (11,736 products)
├── charts/                   # Generated visualizations
│   ├── 01_top_brands.png
│   ├── 02_price_by_category.png
│   ├── 03_discount_distribution.png
│   ├── 04_top_sellers.png
│   ├── 05_price_ranges.png
│   ├── 06_seller_ratings.png
│   ├── 07_installment_options.png
│   ├── 08_rating_vs_price.png
│   ├── 09_top_categories.png
│   └── 10_brand_market_share.png
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## License

MIT

---

**Last Updated**: December 2025
**Data Source**: Umico Marketplace API
**Total Products Analyzed**: 11,712
