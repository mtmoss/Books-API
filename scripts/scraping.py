import csv
import time
import re
from pathlib import Path
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup

BASE = "http://books.toscrape.com/"
SAIDA_CSV = Path("data/livros.csv")

LIMITE_PAGINAS = 2

def extrair_preco(texto: str) -> float:
    return float(re.sub(r"[^0-9.]", "", texto))

MAPA_NOTA = {
    "One": 1.0,
    "Two": 2.0,
    "Three": 3.0,
    "Four": 4.0,
    "Five": 5.0
}

def extrair_nota(div_rating) -> float:
    for nome in MAPA_NOTA:
        if nome in div_rating.get("class", []):
            return MAPA_NOTA[nome]
    return 0.0

def extrair_disponivel(texto: str) -> int:
    m = re.search(r"(\d+)\s+available\)", texto)
    return int(m.group(1)) if m else 0

def obter_sopa(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def url_genero(nome_href: str) -> str:
    return f"{BASE}/{nome_href}"

def url_proxima_pagina(url_atual: str, sopa: BeautifulSoup) -> Optional[str]:
    li_next = sopa.select_one("li.next > a")
    if not li_next:
        return None
    href = li_next.get("href")
    if not href:
        return None
    if url_atual.endswith("index.html"):
        base = url_atual.rsplit("/", 1)[0]
        return  f"{base}/{href}"
    return f"{BASE}/{ href}"

def extrair_livros_da_pagina(sopa: BeautifulSoup, genero_atual: str) -> List[Dict]:
    itens = []
    for artigo in sopa.select("article.product_pod"):
        titulo = artigo.h3.a.get("title", "").strip()
        link_rel = artigo.h3.a.get("href", "")
        link = link_rel
        if link and not link.startswith("http"):
            if link_rel.startswith("../"):
                link = f"{BASE}catalogue/{link_rel.replace('../', '')}"
            else:
                link = f"{BASE}{link_rel}"

        preco_txt = artigo.select_one("p.price_color").text.strip()
        preco = extrair_preco(preco_txt)

        nota = extrair_nota(artigo.select_one("p.star-rating"))

        detalhe = obter_sopa(link)
        disp_txt = detalhe.select_one("p.instock.availability").text.strip()
        disponivel = extrair_disponivel(disp_txt)

        img_rel = detalhe.select_one("div.item.active > img").get("src", "")
        if img_rel.startswith("../"):
            imagem = f"{BASE}{img_rel.replace('../', '')}"
        else:
            imagem = f"{BASE}{img_rel}"

        itens.append({
            "titulo": titulo,
            "preco": preco,
            "nota": nota,
            "disponivel": disponivel,
            "genero": genero_atual,
            "imagem": imagem
        })
        time.sleep(0.2)
    return itens

def coletar_livros() -> List[Dict]:
    raiz = obter_sopa(BASE)
    links_generos = raiz.select("div.side_categories ul li ul li a")[:5]

    todos: List[Dict] = []
    for a in links_generos:
        nome = a.text.strip()
        href = a.get("href")
        url = url_genero(href)
        paginas = 0

        while url and paginas < LIMITE_PAGINAS:
            sopa = obter_sopa(url)
            todos.extend(extrair_livros_da_pagina(sopa, genero_atual=nome))
            paginas += 1
            url = url_proxima_pagina(url, sopa)
            time.sleep(0.2)

    for i, d in enumerate(todos, start=1):
        d["id"] = i
    return todos

def salvar_csv(livros: List[Dict], caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    campos = ["id", "titulo", "preco", "nota", "disponivel", "genero", "imagem"]
    with caminho.open("w", encoding="utf-8", newline="") as arq:
        escritor = csv.DictWriter(arq, fieldnames=campos)
        escritor.writeheader()
        for d in livros:
            escritor.writerow({c: d.get(c) for c in campos})

if __name__ == "__main__":
    livros = coletar_livros()
    salvar_csv(livros, SAIDA_CSV)
    print(f"Coleta concluída: {len(livros)} livros salvos em {SAIDA_CSV}")