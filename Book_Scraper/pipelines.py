# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class BookScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            price_str = adapter['price']
            price_value = float(price_str.replace('£', '').strip())
            adapter['price'] = price_value
        
        if adapter.get('availability'):
            availability_str = adapter['availability']
            stock_match = re.search(r'\((\d+)', availability_str)
            if stock_match:
                adapter['stock'] = int(stock_match.group(1))
            elif 'In stock' in availability_str:
                adapter['stock'] = 1
            else:
                adapter['stock'] = 0
        
        if adapter.get('rating'):
            rating_map = {
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
            }
            adapter['rating'] = rating_map.get(adapter['rating'], 0)
        
        if adapter.get('tax'):
                tax_str = adapter['tax']
                tax_clean = re.sub(r'[^\d.]', '', tax_str)
                adapter['tax'] = float(tax_clean) if tax_clean else 0.0
        
        if adapter.get('number_of_reviews'):
            try:
                adapter['number_of_reviews'] = int(adapter['number_of_reviews'])
            except (ValueError, TypeError):
                adapter['number_of_reviews'] = 0
        
        if adapter.get('upc'):
            adapter['upc'] = adapter['upc'].strip()
        
        return item