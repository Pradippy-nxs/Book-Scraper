import json
from collections import defaultdict
from typing import List, Dict, Any


class BooksQuery:
    def __init__(self, json_file='books_data.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.books = json.load(f)
        print(f"📚 Loaded {len(self.books)} books from {json_file}")
    
    def filter_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        result = [
            book for book in self.books
            if min_price <= book.get('price', 0) <= max_price
        ]
        return result
    
    def filter_by_category(self, category: str) -> List[Dict]:
        category_lower = category.lower()
        result = [
            book for book in self.books
            if book.get('category', '').lower() == category_lower
        ]
        return result
    
    def filter_by_rating(self, min_rating: int) -> List[Dict]:
        result = [
            book for book in self.books
            if book.get('rating', 0) >= min_rating
        ]
        return result
    
    def get_categories(self) -> Dict[str, int]:
        categories = defaultdict(int)
        for book in self.books:
            cat = book.get('category', 'Unknown')
            categories[cat] += 1
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def get_average_price_by_category(self, category: str) -> float:
        """Hitung rata-rata harga buku dalam kategori tertentu"""
        books_in_category = self.filter_by_category(category)
        if not books_in_category:
            return 0.0
        
        total_price = sum(book.get('price', 0) for book in books_in_category)
        return total_price / len(books_in_category)
    
    def get_statistics(self) -> Dict[str, Any]:
        prices = [book.get('price', 0) for book in self.books]
        ratings = [book.get('rating', 0) for book in self.books]
        
        stats = {
            'total_books': len(self.books),
            'total_categories': len(self.get_categories()),
            'price': {
                'min': min(prices) if prices else 0,
                'max': max(prices) if prices else 0,
                'average': sum(prices) / len(prices) if prices else 0,
            },
            'rating': {
                'average': sum(ratings) / len(ratings) if ratings else 0,
            },
            'availability': {
                'in_stock': sum(1 for b in self.books if b.get('stock', 0) > 0),
                'out_of_stock': sum(1 for b in self.books if b.get('stock', 0) == 0),
            }
        }
        return stats


def main():
    print("=" * 70)
    print("📖 BOOKS QUERY TOOL - books.toscrape.com")
    print("=" * 70)
    print()
    
    query = BooksQuery('books_data.json')
    
    # Query 1: Berapa buku dengan harga 40-50 pounds?
    print("🔍 Query 1: Buku dengan harga antara £40-50")
    books_40_50 = query.filter_by_price_range(40.0, 50.0)
    print(f"   Jumlah: {len(books_40_50)} buku")
    for book in books_40_50[:5]:  # Show first 5
        print(f"   - {book['title']}: £{book['price']:.2f}")
    if len(books_40_50) > 5:
        print(f"   ... dan {len(books_40_50) - 5} buku lainnya")
    print()
    
    # Query 2: Semua kategori
    print("🔍 Query 2: Semua kategori buku dan jumlahnya")
    categories = query.get_categories()
    for i, (cat, count) in enumerate(categories.items(), 1):
        print(f"   {i}. {cat}: {count} buku")
    print()
    
    # Query 3: Buku Fiction
    print("🔍 Query 3: Berapa buku kategori 'Fiction'?")
    fiction_books = query.filter_by_category('Fiction')
    print(f"   Jumlah: {len(fiction_books)} buku")
    print()
    
    # Query 4: Rata-rata harga buku Music
    print("🔍 Query 4: Rata-rata harga buku kategori 'Music'")
    music_avg = query.get_average_price_by_category('Music')
    print(f"   Rata-rata: £{music_avg:.2f}")
    print()
    
    # Query 5: Buku dengan rating tinggi (4-5)
    print("🔍 Query 5: Buku dengan rating minimal 4")
    high_rated = query.filter_by_rating(4)
    print(f"   Jumlah: {len(high_rated)} buku")
    print()
    
    # Query 6: Statistik umum
    print("🔍 Query 6: Statistik Umum")
    stats = query.get_statistics()
    print(f"   Total buku: {stats['total_books']}")
    print(f"   Total kategori: {stats['total_categories']}")
    print(f"   Harga terendah: £{stats['price']['min']:.2f}")
    print(f"   Harga tertinggi: £{stats['price']['max']:.2f}")
    print(f"   Rata-rata harga: £{stats['price']['average']:.2f}")
    print(f"   Rata-rata rating: {stats['rating']['average']:.1f}")
    print(f"   Buku tersedia: {stats['availability']['in_stock']}")
    print(f"   Buku habis: {stats['availability']['out_of_stock']}")
    print()
    
    print("=" * 70)
    print("✅ Query selesai!")
    print("=" * 70)


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("❌ Error: File 'books_data.json' tidak ditemukan!")
        print("   Jalankan scraping terlebih dahulu dengan:")
        print("   scrapy crawl books")
    except Exception as e:
        print(f"❌ Error: {e}")