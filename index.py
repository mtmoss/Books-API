from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes.health import route_health
from api.routes.books import route_books

app = FastAPI(
    title="Book Scraping API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=302)

app.include_router(route_health)
app.include_router(route_books)