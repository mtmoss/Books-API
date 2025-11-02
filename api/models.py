from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    available: int
    category: str
    image: str

class OutputBooks(BaseModel):
    total: int
    items: List[Book]