# Books-API

API pública de consulta de livros (FastAPI).

## Rodar localmente
poetry env activate
poetry run uvicorn api.index:app --reload

Abrir Swagger: http://127.0.0.1:8000/docs

## Endpoints
GET /api/v1/health
GET /api/v1/books
GET /api/v1/books/{id}
GET /api/v1/books/search?titulo=&genero=
GET /api/v1/generos

## Autenticação (bônus)
POST /api/v1/auth/login
GET  /api/v1/auth/eu  (enviar Authorization: Bearer <token>)