import os
from fastapi import FastAPI
from api.routes.health import route_health
from api.routes.books import route_books
from api.routes.auth import route_auth

VERCEL_BASE_ROUTE = "/api" if os.getenv("VERCEL") else ""

app = FastAPI(
    title="Book Scraping API",
    version="1.0.0"
)

app.include_router(route_health)
app.include_router(route_books)
app.include_router(route_auth)