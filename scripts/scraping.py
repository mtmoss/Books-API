import csv
import time
import re
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random

import requests
from bs4 import BeautifulSoup

BASE = "http://books.toscrape.com/"
CSV_OUTPUT = Path("data/books.csv")
SESSION = requests.Session()
RETRY = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=0.6,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
    raise_on_status=False
)

ADAPTER = HTTPAdapter(max_retries=RETRY, pool_connections=50, pool_maxsize=50)
SESSION.mount("http://", ADAPTER)
SESSION.mount("https://", ADAPTER)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

def get_price(text: str) -> float:
    return float(re.sub(r"[^0-9.]", "", text))

MAP_RATING = {
    "One": 1.0,
    "Two": 2.0,
    "Three": 3.0,
    "Four": 4.0,
    "Five": 5.0
}

def get_rating(div_rating) -> float:
    for name in MAP_RATING:
        if name in div_rating.get("class", []):
            return MAP_RATING[name]
    return 0.0

def get_available(text: str) -> int:
    m = re.search(r"(\d+)\s+available\)", text)
    return int(m.group(1)) if m else 0

def get_soup(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = SESSION.get(url, headers=DEFAULT_HEADERS, timeout=(10, 25))
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"Falha em {url} -> {e}")
        return None
    finally:
        time.sleep(0.15 + random.random() * 0.25)

def url_category(name_href: str) -> str:
    return urljoin(BASE, name_href)

def url_next_page(current_url: str, soup: BeautifulSoup) -> Optional[str]:
    a = soup.select_one("li.next a")
    if not a:
        return None
    href = a.get("href", "")
    if not href:
        return None
    return urljoin(current_url, href)

def get_books_from_page(soup: BeautifulSoup, current_category: str, page_url: str) -> List[Dict]:
    items = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a.get("title", "").strip()
        link_rel = article.h3.a.get("href", "")
        link = urljoin(page_url, link_rel)

        price_txt = article.select_one("p.price_color").text.strip()
        price = get_price(price_txt)

        rating = get_rating(article.select_one("p.star-rating"))

        detail = get_soup(link)
        if detail is None:
            continue

        avail_el = detail.select_one("p.instock.availability")
        if not avail_el:
            available = 0
        else:
            avail_txt = avail_el.text.strip()
            available = get_available(avail_txt)

        img_el = detail.select_one("div.item.active > img")
        if img_el:
            image_rel = img_el.get("src", "")
            image = urljoin(link, image_rel)
        else:
            image = ""

        items.append({
            "title": title,
            "price": price,
            "rating": rating,
            "available": available,
            "category": current_category,
            "image": image
        })
    return items

def get_books() -> List[Dict]:
    root = get_soup(BASE)
    links_categories = root.select("div.side_categories ul li ul li a")

    all_books: List[Dict] = []
    for a in links_categories:
        name = a.text.strip()
        href = a.get("href")
        url = url_category(href)
        pages = 0
        while url:
            pages += 1
            soup = get_soup(url)
            if soup is None:
                break
            all_books.extend(get_books_from_page(soup, name, url))
            url = url_next_page(url, soup)
            time.sleep(0.6 + random.random() * 0.6)

    for i, d in enumerate(all_books, start=1):
        d["id"] = i
    return all_books

def write_csv(books: List[Dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "title", "price", "rating", "available", "category", "image"]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for d in books:
            writer.writerow({c: d.get(c) for c in fields})

if __name__ == "__main__":
    books = get_books()
    write_csv(books, CSV_OUTPUT)
    print(f"Coleta concluída: {len(books)} livros salvos em {CSV_OUTPUT}")