import asyncio
import aiohttp
import csv
import math
from typing import List, Dict, Any
from datetime import datetime
import json

# Configuration
BASE_URL = "https://mp-catalog.umico.az/api/v1/products"
CATEGORY_ID = 15
PER_PAGE = 24
SORT = "global_popular_score"
MAX_CONCURRENT_REQUESTS = 10  # Limit concurrent requests to be respectful
OUTPUT_FILE = "umico_products.csv"

# Headers to mimic browser request
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "az",
    "content-language": "az",
    "origin": "https://birmarket.az",
    "referer": "https://birmarket.az/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
}

class UmicoScraper:
    def __init__(self):
        self.session = None
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.all_products = []
        self.failed_pages = []

    async def fetch_page(self, page: int, retries: int = 3) -> Dict[str, Any]:
        """Fetch a single page with retry logic"""
        url = f"{BASE_URL}?page={page}&category_id={CATEGORY_ID}&per_page={PER_PAGE}&sort={SORT}"

        for attempt in range(retries):
            try:
                async with self.semaphore:
                    async with self.session.get(url, headers=HEADERS, timeout=30) as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"✓ Page {page} fetched successfully ({len(data.get('products', []))} products)")
                            return data
                        else:
                            print(f"✗ Page {page} returned status {response.status}")

            except asyncio.TimeoutError:
                print(f"⚠ Page {page} timeout (attempt {attempt + 1}/{retries})")
            except Exception as e:
                print(f"⚠ Page {page} error: {str(e)} (attempt {attempt + 1}/{retries})")

            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        self.failed_pages.append(page)
        return {"products": []}

    def flatten_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested product structure for CSV"""
        default_offer = product.get('default_offer', {})
        seller = default_offer.get('seller', {})
        marketing_name = seller.get('marketing_name', {})
        category = product.get('category', {})
        ratings = product.get('ratings', {})
        main_img = product.get('main_img', {})

        # Extract product labels
        labels = product.get('product_labels', [])
        label_names = ', '.join([label.get('name', '') for label in labels]) if labels else ''

        return {
            'product_id': product.get('id'),
            'name': product.get('name'),
            'slugged_name': product.get('slugged_name'),
            'status': product.get('status'),
            'brand': product.get('brand'),
            'category_id': category.get('id'),
            'category_name': category.get('name'),
            'old_price': default_offer.get('old_price'),
            'retail_price': default_offer.get('retail_price'),
            'discount_percent': round(((default_offer.get('old_price', 0) - default_offer.get('retail_price', 0)) / default_offer.get('old_price', 1)) * 100, 2) if default_offer.get('old_price') else 0,
            'installment_enabled': default_offer.get('installment_enabled'),
            'max_installment_months': default_offer.get('max_installment_months'),
            'seller_id': seller.get('ext_id'),
            'seller_name': marketing_name.get('name'),
            'seller_rating': seller.get('rating'),
            'seller_role': seller.get('role_name'),
            'seller_vat_payer': seller.get('vat_payer'),
            'rating_value': ratings.get('rating_value'),
            'rating_count': ratings.get('session_count'),
            'min_qty': product.get('min_qty'),
            'preorder_available': product.get('preorder_available'),
            'product_labels': label_names,
            'image_small': main_img.get('small'),
            'image_medium': main_img.get('medium'),
            'image_big': main_img.get('big'),
            'offer_uuid': default_offer.get('uuid'),
            'stock_qty': default_offer.get('qty'),
            'discount_start_date': default_offer.get('discount_effective_start_date'),
            'discount_end_date': default_offer.get('discount_effective_end_date'),
        }

    async def scrape_all_pages(self):
        """Scrape all pages concurrently"""
        # Create aiohttp session
        connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS, force_close=True)
        timeout = aiohttp.ClientTimeout(total=60)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

        try:
            # Fetch first page to get total count
            print("Fetching first page to determine total pages...")
            first_page_data = await self.fetch_page(1)
            total_products = first_page_data.get('meta', {}).get('total', 0)
            total_pages = math.ceil(total_products / PER_PAGE)

            print(f"\n{'='*60}")
            print(f"Total products: {total_products}")
            print(f"Total pages: {total_pages}")
            print(f"Products per page: {PER_PAGE}")
            print(f"Max concurrent requests: {MAX_CONCURRENT_REQUESTS}")
            print(f"{'='*60}\n")

            # Add first page products
            for product in first_page_data.get('products', []):
                self.all_products.append(self.flatten_product(product))

            # Create tasks for remaining pages
            tasks = []
            for page in range(2, total_pages + 1):
                tasks.append(self.fetch_page(page))

            # Fetch all pages concurrently with progress tracking
            print(f"Fetching pages 2-{total_pages}...\n")
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for result in results:
                if isinstance(result, dict):
                    for product in result.get('products', []):
                        self.all_products.append(self.flatten_product(product))

            print(f"\n{'='*60}")
            print(f"Scraping completed!")
            print(f"Total products scraped: {len(self.all_products)}")
            print(f"Failed pages: {len(self.failed_pages)}")
            if self.failed_pages:
                print(f"Failed page numbers: {self.failed_pages}")
            print(f"{'='*60}\n")

        finally:
            await self.session.close()

    def save_to_csv(self):
        """Save scraped data to CSV"""
        if not self.all_products:
            print("No products to save!")
            return

        print(f"Saving {len(self.all_products)} products to {OUTPUT_FILE}...")

        # Get all unique keys from products
        fieldnames = list(self.all_products[0].keys())

        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.all_products)

        print(f"✓ Data saved successfully to {OUTPUT_FILE}")

        # Also save failed pages for retry if needed
        if self.failed_pages:
            with open('failed_pages.json', 'w') as f:
                json.dump(self.failed_pages, f)
            print(f"✓ Failed pages saved to failed_pages.json")

async def main():
    start_time = datetime.now()
    print(f"Starting Umico scraper at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    scraper = UmicoScraper()
    await scraper.scrape_all_pages()
    scraper.save_to_csv()

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{'='*60}")
    print(f"Scraping completed in {duration:.2f} seconds")
    print(f"Average time per page: {duration / (math.ceil(11713 / 24)):.2f} seconds")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
