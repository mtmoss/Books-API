import csv
from pathlib import Path
from typing import List, Dict, Optional
from .models import Book

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data/books.csv"

_books_memory: List[Dict] = [
    {
        "id": 1,
        "title": "A Light in the Attic",
        "price": 51.77,
        "rating": 3.0,
        "available": 22,
        "category": "Poetry",
        "image": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
    },
    {
        "id": 2,
        "title": "Tipping the Velvet",
        "price": 53.74,
        "rating": 1.0,
        "available": 8,
        "category": "Historical Fiction",
        "image": "https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
    }
]

def list_books() -> List[Book]:
    csv_items = load_from_csv()
    if csv_items:
        return csv_items
    return [Book(**d) for d in _books_memory]

def get_book_by_id(id: int) -> Optional[Book]:
    for book in list_books():
        if book.id == id:
            return book
    return None

def list_categories() -> List[str]:
    return sorted({book.category for book in list_books()})

def load_from_csv() -> List[Book]:
    if not CSV_PATH.exists():
        return []
    items: List[Book] = []
    with CSV_PATH.open("r", encoding="utf-8") as arq:
        reader = csv.DictReader(arq)
        for row in reader:
            items.append(Book(
                id=int(row["id"]),
                title=row["title"],
                price=float(row["price"]),
                rating=float(row["rating"]),
                available=int(row["available"]),
                category=row["category"],
                image=row["image"]
            ))
    return items