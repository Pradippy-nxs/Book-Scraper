# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookScraperItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    price_currency = scrapy.Field()
    price_excl_tax = scrapy.Field()     
    price_incl_tax = scrapy.Field()     
    tax = scrapy.Field()                
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()  
    availability = scrapy.Field()
    stock = scrapy.Field()
    upc = scrapy.Field()                
    product_type = scrapy.Field()       
    description = scrapy.Field()
    image_url = scrapy.Field()
