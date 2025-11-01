# 📚 Book Scraping API

# Books API

Tech Challenge da Fase 1 da pós-graduação em **Machine Learning Engineering** (FIAP).  
API RESTful desenvolvida em **FastAPI** para fazer web scraping do catálogo de livros em https://books.toscrape.com/. Traz endpoints públicos para consulta do catálogo. O projeto está preparado para rodar localmente (Uvicorn) e em produção na **Vercel**.

> **Produção:** https://books-api-lilac.vercel.app/ (Redireciona para a documentação Swagger)
>
> **Vídeo de apresentação:** ...

---

## Arquitetura

- **FastAPI** como framework web (ASGI).  
- **Uvicorn** como servidor de desenvolvimento.  
- **Routers** organizando os endpoints (ex.: `status`, `books` e, opcionalmente, `auth`).  
- **Camada de dados** simples (em memória e/ou arquivos em `data/`).  
- **Autenticação** via **JWT** (opcional), usando `pyjwt`.  
- **Vercel** para deploy, com roteamento configurado para expor o Swagger em produção.

---

## Stack e dependências

- **Python ≥ 3.12**
- **FastAPI**
- **Uvicorn**
- **Pydantic** (modelagem/validação)
- **PyJWT** (opcional, para autenticação JWT)
- **Requests / BeautifulSoup4** (utilidades de integração/extração)
- **Poetry 2.2.1** (lockfile presente) ou `requirements.txt`

---

## Estrutura de pastas

```
Books-API/
├─ api/                 # Código da aplicação (routers, modelos, inicialização do FastAPI)
├─ data/                # Arquivos de dados (o .csv extraído do scraping)
├─ scripts/             # Script de web scraping
├─ requirements.txt     # Lista de dependências para deploy
├─ poetry.lock          # Lockfile do Poetry (gerado com 2.2.1)
├─ vercel.json          # Configuração de roteamento para produção
└─ README.md
```

> Em produção, a raiz (`/`) redireciona para `/docs` (Swagger). Configurado no `vercel.json`.

---

## Instalação e configuração

### 1) Clonar o repositório
```bash
git clone https://github.com/mtmoss/Books-API.git
cd Books-API
```

### 2a) Ambiente com **Poetry** (recomendado)
> Requer Poetry 2.2.1+ já instalado.

```bash
poetry install
poetry run python -V        # conferir versão
```

### 2b) Ambiente com **venv + pip** (alternativa)
```bash
python3 -m venv .venv
source .venv/bin/activate   # no macOS/Linux
# .venv\Scripts\activate  # no Windows PowerShell

pip install -r requirements.txt
```

### 3) Variáveis de ambiente (se usar JWT)
Crie um arquivo `.env` (ou exporte as variáveis no shell) com os valores necessários:

```
JWT_SECRET=troque-este-segredo
JWT_ALG=HS256
JWT_EXP_MIN=60
```

> Se sua aplicação não exige autenticação, esta etapa pode ser ignorada.

---

## Execução local

> O módulo principal expõe um objeto `app` do FastAPI. Ajuste o caminho abaixo conforme o arquivo/módulo do seu projeto.

```bash
# Exemplo: se o arquivo de entrada for api/index.py com 'app' definido
uvicorn api.index:app --reload --port 8000
```

Acesse:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

---

## Documentação da API (Swagger/OpenAPI)

- **Produção:** https://books-api-lilac.vercel.app/docs  
- **Local:** http://127.0.0.1:8000/docs

A especificação OpenAPI reflete fielmente os endpoints ativos, seus parâmetros, corpos e respostas. Use o Swagger para testar as rotas rapidamente.

---

## Rotas e Endpoints

> **Atenção:** a lista abaixo serve como guia. Consulte o Swagger para a cobertura total e atualizada das rotas ativas no deploy.

### Status / Healthcheck
- `GET /status` — retorna informações básicas de saúde do serviço (ex.: `{"status": "ok"}`).

### Livros
- `GET /books` — lista de livros. Pode retornar campos como: `id`, `titulo`, `preco`, `nota`, `disponivel`, `genero`, `imagem`.
- `GET /books/{id}` — detalhes de um livro específico pelo `id`.

### Autenticação (JWT)
> Opcional — habilite apenas se sua aplicação exigir endpoints protegidos.

- `POST /token` — emite um token **JWT** a partir de credenciais mínimas (por exemplo, `username`/`password` ou `client_name`/`client_email`, conforme implementação).  
  **Resposta:** `{ "access_token": "<jwt>", "token_type": "bearer" }`

- Endpoints protegidos devem ser chamados com `Authorization: Bearer <token>`.

---

## Exemplos de requisição e resposta

### 1) Healthcheck
**Requisição**
```bash
curl -i https://books-api-lilac.vercel.app/status
```
**Resposta (exemplo)**
```json
{
  "status": "ok"
}
```

### 2) Listar livros
**Requisição**
```bash
curl -s https://books-api-lilac.vercel.app/books
```
**Resposta (exemplo)**
```json
[
  {
    "id": 1,
    "titulo": "A Light in the Attic",
    "preco": 51.77,
    "nota": 3.0,
    "disponivel": 22,
    "genero": "Poetry",
    "imagem": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
  }
]
```

### 3) Obter livro por ID
**Requisição**
```bash
curl -s https://books-api-lilac.vercel.app/books/1
```

### 4) Autenticação e uso de rota protegida
**Obter token**
```bash
curl -s -X POST https://books-api-lilac.vercel.app/token   -H "Content-Type: application/json"   -d '{"username":"demo","password":"demo"}'
```
**Resposta (exemplo)**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

**Chamar rota protegida**
```bash
curl -s https://books-api-lilac.vercel.app/orders   -H "Authorization: Bearer eyJhbGciOi..."
```

> Ajuste os nomes das rotas protegidas de acordo com o que estiver definido no seu Swagger.

---

## Testes rápidos

1. Acesse o Swagger em produção: `https://books-api-lilac.vercel.app/docs`  
2. Clique em **Authorize** (se houver segurança configurada) e informe o token.  
3. Execute `GET /status` e `GET /books` para validar o funcionamento.  
4. Verifique respostas HTTP (`200`, `401/403` se proteção ativa, etc.).

---

## Deploy na Vercel

- Projeto preparado com `vercel.json`, incluindo redirecionamento da raiz para `/docs`.  
- Cada push no branch configurado dispara um deploy automático (caso o projeto esteja conectado na Vercel).

### Passos resumidos
1. Crie o projeto na Vercel e conecte ao repositório GitHub.  
2. Defina as **variáveis de ambiente** (se usar JWT).  
3. Confirme a versão do **Python** e o comando de build se necessário (normalmente, FastAPI em Vercel usa a detecção automática + `requirements.txt`).  
4. Após o deploy, valide o Swagger em `/docs` e os endpoints principais.