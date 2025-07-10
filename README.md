# 📚 Books Scraper

Este scraper recorre el sitio [books.toscrape.com](https://books.toscrape.com), accede a **cada libro individual**, y extrae:

- Título
- Precio con impuestos
- Disponibilidad en stock
- Código UPC

Todos estos datos se almacenan en un archivo `.csv` llamado `books_scraped.csv`.

## 📦 Requisitos

- Python 3.11.9
- requests
- BeautifulSoup4
- urllib.parse

## 🚀 Cómo usar

1. Cloná el repositorio o copiá el script `books_scraper.py`
2. Ejecutá el script:

```bash
python books_scraper.py
