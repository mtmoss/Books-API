import os
from fastapi import FastAPI
from books_api.rotas.saude import rota_saude
from books_api.rotas.livros import rota_livros
from books_api.rotas.autenticacao import rota_autenticacao

ROTA_BASE_VERCEL = "/api" if os.getenv("VERCEL") else ""

app = FastAPI(
    title="Books API",
    version="1.0.0",
    servers=[{"url": ROTA_BASE_VERCEL}]
)

app.include_router(rota_saude)
app.include_router(rota_livros)
app.include_router(rota_autenticacao)