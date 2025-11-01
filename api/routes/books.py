from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models import Book, OutputBooks
from ..repository import get_book_by_id, list_books, list_categories
from ..services import filter_books

route_books = APIRouter(prefix="/api/v1", tags=["books"])

@route_books.get("/books", response_model=OutputBooks)
def list_all_books():
    items = list_books()
    return {"total": len(items), "items": items}

@route_books.get("/books/search", response_model=OutputBooks)
def search_books(
    title: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None)
):
    items = list_books()
    items_filter = filter_books(items, title=title, category=category)
    return {"total": len(items_filter), "items": items_filter}

@route_books.get("/books/{id}", response_model=Book)
def detail_book(id: int):
    book = get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

@route_books.get("/books/categories", response_model=List[str])
def get_categories():
    return list_categories()