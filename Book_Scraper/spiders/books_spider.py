from pathlib import Path

import scrapy

strArr_genres = ["Travel",
    "Mystery",
    "Historical Fiction",
    "Sequential Art",
    "Classics",
    "Philosophy",
    "Romance",
    "Womens Fiction",
    "Fiction",
    "Childrens",
    "Religion",
    "Nonfiction",
    "Music",
    "Default",
    "Science Fiction",
    "Sports and Games",
    "Add a comment",
    "Fantasy",
    "New Adult",
    "Young Adult",
    "Science",
    "Poetry",
    "Paranormal",
    "Art",
    "Psychology",
    "Autobiography",
    "Parenting",
    "Adult Fiction",
    "Humor",
    "Horror",
    "History",
    "Food and Drink",
    "Christian Fiction",
    "Business",
    "Biography",
    "Thriller",
    "Contemporary",
    "Spirituality",
    "Academic",
    "Self Help",
    "Historical",
    "Christian",
    "Suspense",
    "Short Stories",
    "Novels",
    "Health",
    "Politics",
    "Cultural",
    "Erotica",
    "Crime"]

str_link_prefix = "https://books.toscrape.com/catalogue/category/books/"
str_link_postfix = "/index.html"

def strArr_link_maker():
    strArr_links = []
    for i in range(len(strArr_genres)):
        strArr_links.append(str_link_prefix + str(strArr_genres[i].lower())+ "_" + str((i+2))+str_link_postfix)
    return strArr_links


print(strArr_link_maker())


class QuotesSpider(scrapy.Spider):

    name = "books"
    async def start(self):
        urls = strArr_link_maker()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")