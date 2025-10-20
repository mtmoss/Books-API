from fastapi import FastAPI
from books_api.rotas.saude import rota_saude

app = FastAPI(title="Books API", version="1.0.0")

app.include_router(rota_saude)