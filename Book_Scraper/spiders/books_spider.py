from pathlib import Path

import scrapy

genres = ["Travel",
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

# Link base 
link_prefix = "https://books.toscrape.com/catalogue/category/books/"
link_postfix = "/index.html"

# Replace spaces with dashes 
# Can be refactored to be more performant/clean
def space_replacer(genres):
    filtered_genres = []
    for genre in genres:
        temp = ""
        for character in genre:
            if character == ' ':
                temp += '-'
            else:
                temp += character
        filtered_genres.append(temp)
    return filtered_genres

# Makes the link for the spider to use
def link_maker(filtered):
    links = []
    for i in range(len(filtered)):
        links.append(link_prefix + str(filtered[i].lower())+ "_" + str((i+2))+link_postfix)
    return links

#Filter function to see the rating
def rating_filter(rating):
    # quantity = ["One", "Two", "Three", "Four", "Five"]
    word_to_delete = "star-rating "
    current_word = ""
    for character in rating:
        # if current_word not in quantity:
        if current_word == word_to_delete:
            current_word = ""
        current_word += character
    return current_word + " star"
# print(link_maker(space_replacer(genres)))

def status_filter(status):
    word_to_return = "instock"
    current_word = ""
    for character in status:
        if current_word != word_to_return:
            current_word += character
        else:
            return "In stock"

class QuotesSpider(scrapy.Spider):

    name = "books"
    start_urls = ["https://books.toscrape.com/catalogue/category/books/crime_51/index.html"]
    # start_urls = link_maker(space_replacer(genres))

    def parse(self, response):

        # Generate html files 
        # page = response.url.split("/")[-2]
        # filename = f"books-{page}.html"
        # Path(filename).write_bytes(response.body)

        # Parse data 
        genre = response.css("div ul.breadcrumb li.active::text").get()
        for book in response.css("article.product_pod"):
            yield {
                "Title": book.css("h3 a::attr(title)").get(),
                "Rating": rating_filter(book.css("p.star-rating::attr(class)").get()),
                "Genre": genre,
                "Price": book.css("p.price_color::text").get(),
                "Status": status_filter(book.css("p.instock::attr(class)").get()),
            }