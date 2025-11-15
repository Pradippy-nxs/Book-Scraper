How to scrape:
scrapy crawl books

How to scrape and store:
scrapy crawl books -O books.json

File structure:
```
Book_Scraper/
│
├── Book_Scraper/
│   ├── spiders/
│   │   ├── books_spider.py
│   │   ├── __init__.py
│   │   └── __pycache__/ (.gitignored)
│   │
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   ├── __init__.py
│   └── __pycache__/ (.gitignored)
│
├── venv/ (.gitignored)
│
├── scrapy.cfg
├── requirements.txt
├── README.md
└── .gitignore

```