import scrapy
import json

class SrealitySpider(scrapy.Spider):
    name = 'sreality'
    allowed_domains = ['sreality.cz']
    start_urls = [
        'https://www.sreality.cz/api/en/v2/estates?category_main_cb=2&category_type_cb=1&locality_region_id=10&page=1&per_page=100'
    ]  

    custom_settings = {
        'FEEDS': {
            '../data/estates.csv': {
                'format': 'csv',
                'fields': ['title', 'image_urls', 'price']
            }
        }
    }

    items_yielded = 0  # Initialize a counter for yielded items

    def parse(self, response):
        """
        Parses the response from estate listing API, extracts and yields estate information 
        until 500 valid items are reached or all pages have been processed. Skips estates 
        without a valid price and automatically fetches the next page if under the item limit.
        """
        if self.items_yielded >= 500:
            # If 500 items have been yielded, do not process further pages
            return

        data = json.loads(response.text)
        estates = data.get('_embedded', {}).get('estates', [])
        for estate in estates:
            if self.items_yielded >= 500:
                # Stop if 500 valid items have been collected
                break

            title = estate.get('name', '')
            image_urls = self.extract_image_urls(estate)
            price = self.extract_price(estate)

            if price is None or price.strip() == '0':
                # Skip estates with a price of 0 or when price is not available
                continue

            self.items_yielded += 1  # Increment the counter for each valid item
            yield {
                'title': title,
                'image_urls': image_urls,
                'price': price
            }

        # Check if more pages should be fetched
        if self.items_yielded < 500:
            current_page = data.get('paging', {}).get('page', 0)
            total_pages = data.get('paging', {}).get('total_pages', 1)
            if current_page < total_pages:
                next_page = current_page + 1
                next_page_url = f"https://www.sreality.cz/api/en/v2/estates?category_main_cb=2&category_type_cb=1&locality_region_id=10&page={next_page}&per_page=500"
                yield scrapy.Request(next_page_url, callback=self.parse)

    def extract_image_urls(self, estate):
        """
        Extracts and concatenates image URLs from a single estate listing.
        This method navigates the estate data structure to find image links and 
        concatenates them into a single string separated by semicolons.
        """
        image_links = estate.get('_links', {}).get('images', [])
        images = [link.get('href', '') for link in image_links if link.get('href', '')]
        return ';'.join(images)

    def extract_price(self, estate):
        """
        Extracts the price from an estate listing. Handles both dictionary and integer formats
        for the price information. Skips estates with a price of 0 or undefined prices.
        """
        price_info = estate.get('price', {})
        if isinstance(price_info, dict):
            value_raw = price_info.get('value_raw')
            unit = price_info.get('unit', '')
            if value_raw and value_raw != 0:
                return f"{value_raw} {unit}"
            else:
                return None  # Skip prices that are 0
        elif isinstance(price_info, int) and price_info != 0:
            return str(price_info)
        return None
