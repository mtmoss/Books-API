import os
from fastapi import FastAPI
from routes.health import route_health
from routes.books import route_books
from routes.auth import route_auth

VERCEL_BASE_ROUTE = "" if os.getenv("VERCEL") else ""

app = FastAPI(
    title="Book Scraping API",
    version="1.0.0"
)

app.get("/")
def health():
    return {"status": "ok"}

app.include_router(route_health)
app.include_router(route_books)
app.include_router(route_auth)