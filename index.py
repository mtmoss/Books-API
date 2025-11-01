from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes.health import route_health
from api.routes.books import route_books
from api.routes.auth import route_auth

app = FastAPI(
    title="Book Scraping API",
)

app.get("/", include_in_schema=False)
def health():
    return {"status": "ok"}
def root():
    return RedirectResponse("/docs", status_code=307)

app.include_router(route_health)
app.include_router(route_books)
app.include_router(route_auth)