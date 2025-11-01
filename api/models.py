from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    id: int
    title: str
    price: float
    rating: float
    available: int
    category: str
    image: str

class OutputBooks(BaseModel):
    total: int
    items: List[Book]

class UserLogin(BaseModel):
    email: str
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str