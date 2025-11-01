import unicodedata
from typing import Optional, List
from .models import Book

def normalize_text(value: str) -> str:
    if not value:
        return ""
    text = value.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text

def filter_books(
    books: List[Book],
    title: Optional[str] = None,
    category: Optional[str] = None
) -> List[Book]:
    title_n = normalize_text(title or "")
    category_n = normalize_text(category or "")
    result: List[Book] = []

    for book in books:
        title_ok = True
        category_ok = True

        if title_n:
            title_ok = title_n in normalize_text(book.title)

        if category_n:
            category_ok = category_n == normalize_text(book.category)

        if title_ok and category_ok:
            result.append(book)

    return result