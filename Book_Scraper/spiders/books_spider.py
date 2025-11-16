import scrapy
from urllib.parse import urljoin
import re
from Book_Scraper.items import BookScraperItem


class BooksScraper(scrapy.Spider):
    name = "books"
    start_urls = ["http://books.toscrape.com/"]
    allowed_domains = ["books.toscrape.com"]

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 0,
    }

    def __init__(self, category=None, min_price=None, max_price=None, min_rating=None, *args, **kwargs):
        super(BooksScraper, self).__init__(*args, **kwargs)
        
        self.category_filter = category
        
        try:
            self.min_price = float(min_price) if min_price is not None else None
        except (ValueError, TypeError):
            self.min_price = None
            self.logger.warning(f"Invalid min_price value: {min_price}, ignoring filter")
        
        try:
            self.max_price = float(max_price) if max_price is not None else None
        except (ValueError, TypeError):
            self.max_price = None
            self.logger.warning(f"Invalid max_price value: {max_price}, ignoring filter")
        
        try:
            self.min_rating = int(min_rating) if min_rating is not None else None
        except (ValueError, TypeError):
            self.min_rating = None
            self.logger.warning(f"Invalid min_rating value: {min_rating}, ignoring filter")

        self.logger.info(f'Spider initialized with filters:')
        self.logger.info(f"  Category: {self.category_filter or 'All'}")
        self.logger.info(f"  Price Range: £{self.min_price or 0} - £{self.max_price or '∞'}")
        self.logger.info(f"  Min Rating: {self.min_rating or 'Any'}")

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css('h3 a::attr(href)').get()
            if book_url:
                book_url = urljoin(response.url, book_url)
                yield scrapy.Request(book_url, callback=self.parse_book)
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            self.logger.info(f'Navigating to next page: {next_page_url}')
            yield scrapy.Request(next_page_url, callback=self.parse)
    
    def parse_book(self, response):
        item = BookScraperItem()

        # Basic info
        title = response.css('div.product_main h1::text').get()
        item['title'] = title.strip() if title else 'N/A'
        item['url'] = response.url

        # Price info
        price_text = response.css('p.price_color::text').get()
        item['price'] = price_text.strip() if price_text else '£0.00'
        item['price_currency'] = 'GBP'

        # Availability
        availability_text = response.css('p.availability::text').getall()
        if availability_text:
            cleaned_texts = [text.strip() for text in availability_text if text.strip()]
            item['availability'] = cleaned_texts[0] if cleaned_texts else 'Unknown'
        else:
            item['availability'] = 'Unknown'

        # Rating
        rating_class = response.css('p.star-rating::attr(class)').get()
        if rating_class:
            rating = rating_class.replace('star-rating', '').strip()
            item['rating'] = rating
        else:
            item['rating'] = 'Zero'

        # Category
        breadcrumbs = response.css('ul.breadcrumb li')
        if len(breadcrumbs) >= 3:
            category = breadcrumbs[2].css('a::text').get()
            item['category'] = category.strip() if category else 'Unknown'
        else:
            item['category'] = 'Unknown'

        # Product information table
        product_info = {}
        rows = response.css('table.table-striped tr')
        for row in rows:
            key = row.css('th::text').get()
            value = row.css('td::text').get()
            if key and value:
                product_info[key.strip()] = value.strip()
        
        item['upc'] = product_info.get('UPC', '')
        item['product_type'] = product_info.get('Product Type', '')
        item['price_excl_tax'] = product_info.get('Price (excl. tax)', '')
        item['price_incl_tax'] = product_info.get('Price (incl. tax)', '')
        item['tax'] = product_info.get('Tax', '')
        item['number_of_reviews'] = product_info.get('Number of reviews', '0')

        # Description
        description = response.css('article.product_page > p::text').get()
        item['description'] = description.strip() if description else ''
        
        # Image URL
        image_url = response.css('div.item.active img::attr(src)').get()
        if image_url:
            item['image_url'] = urljoin(response.url, image_url)
        else:
            item['image_url'] = ''
        
        if self._should_include_item(item):
            yield item
        else:
            self.logger.debug(f'Item excluded by filters: {item["title"]}')
    
    def _should_include_item(self, item):
        # Category filter
        if self.category_filter:
            category = item.get('category', '')
        if not category or category.lower() != self.category_filter.lower():
            return False
        
        # Price filter
        if self.min_price is not None or self.max_price is not None:
            price_str = item.get('price', '£0.00')
            price_match = re.search(r'[\d.]+', price_str)
            
            if price_match:
                try:
                    price = float(price_match.group())
                except ValueError:
                    self.logger.warning(f"Cannot parse price: {price_str}")
                    return False
            else:
                return False
            
            if self.min_price is not None and price < self.min_price:
                return False
            
            if self.max_price is not None and price > self.max_price:
                return False
        
        if self.min_rating is not None:
            rating_map = {
                'Zero': 0,
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
            }
            rating = rating_map.get(item.get('rating'), 0)
            
            if rating < self.min_rating:
                return False
        
        return True