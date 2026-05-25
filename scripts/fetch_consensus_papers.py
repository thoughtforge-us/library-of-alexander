#!/usr/bin/env python3
"""Fetch research papers from https://consensus.app/library/ and store them locally.
The script:
  1. Downloads the HTML page.
  2. Parses each paper entry for title, authors, year, abstract and PDF link.
  3. Saves the PDF to ~/repos/library-of-alexander/16-research-papers/<sanitized-title>.pdf
  4. Writes a JSON index file `papers_index.json`.
  5. Generates a markdown catalog `README.md`.
"""

import os
import re
import json
import hashlib
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(os.getenv("HOME")) / "repos" / "library-of-alexander"
PAPERS_DIR = ROOT / "16-research-papers"
PAPERS_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = PAPERS_DIR / "papers_index.json"
README_PATH = PAPERS_DIR / "README.md"

BASE_URL = "https://consensus.app"
LIB_URL = f"{BASE_URL}/library/"

def sanitize_filename(name: str) -> str:
    # Remove unsafe characters and limit length
    name = re.sub(r"[\\/:*?\"<>|]", "", name)
    name = name.strip().replace(" ", "_")
    return name[:120]

def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text

def parse_papers(html: str):
    soup = BeautifulSoup(html, "html.parser")
    papers = []
    # The page layout may change; we look for common patterns.
    # Each paper is typically inside a <article> or <div class="paper-item">
    for entry in soup.select("article, div.paper-item"):
        title_tag = entry.select_one("h2, h3, .title")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        # Authors may be in a span or div with class author
        authors_tag = entry.select_one(".authors, .author")
        authors = authors_tag.get_text(strip=True) if authors_tag else ""
        # Year may be present in a small tag
        year_tag = entry.select_one("time, .year")
        year = year_tag.get_text(strip=True) if year_tag else ""
        # Abstract
        abstract_tag = entry.select_one("p.description, .abstract")
        abstract = abstract_tag.get_text(strip=True) if abstract_tag else ""
        # PDF link – look for an <a> with href ending .pdf
        pdf_link = None
        for a in entry.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith('.pdf'):
                pdf_link = href
                break
        if not pdf_link:
            # some entries use a button that loads the PDF via a JS route; skip them
            continue
        # Resolve relative URLs
        pdf_url = pdf_link if pdf_link.startswith('http') else f"{BASE_URL}{pdf_link}"
        papers.append({
            "title": title,
            "authors": authors,
            "year": year,
            "abstract": abstract,
            "pdf_url": pdf_url,
        })
    return papers

def download_pdf(url: str, dest_path: Path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    resp = requests.get(url, headers=headers, stream=True, timeout=60)
    resp.raise_for_status()
    with dest_path.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def main():
    print("Fetching paper list...")
    html = fetch_page(LIB_URL)
    papers = parse_papers(html)
    print(f"Found {len(papers)} papers.")
    index = []
    for p in papers:
        safe_name = sanitize_filename(p["title"])
        pdf_path = PAPERS_DIR / f"{safe_name}.pdf"
        # Download if not already present
        if not pdf_path.exists():
            try:
                print(f"Downloading: {p['title']}")
                download_pdf(p["pdf_url"], pdf_path)
            except Exception as e:
                print(f"  failed ({e}) – skipping")
                continue
        else:
            print(f"Already have: {p['title']}")
        entry = {
            "title": p["title"],
            "authors": p["authors"],
            "year": p["year"],
            "abstract": p["abstract"],
            "pdf_path": str(pdf_path.relative_to(ROOT)),
        }
        index.append(entry)
    # Write JSON index
    with INDEX_PATH.open("w", encoding="utf-8") as jf:
        json.dump(index, jf, indent=2, ensure_ascii=False)
    # Write markdown catalog
    with README_PATH.open("w", encoding="utf-8") as mf:
        mf.write("# Consensus Research Paper Library\n\n")
        mf.write("| Title | Authors | Year | PDF |\n")
        mf.write("|-------|---------|------|-----|\n")
        for e in index:
            title_md = e["title"].replace("|", "\\|")
            authors_md = e["authors"].replace("|", "\\|")
            year_md = e["year"]
            pdf_rel = e["pdf_path"]
            pdf_link = f"[{os.path.basename(pdf_rel)}](file://{Path.home()}/repos/library-of-alexander/{pdf_rel})"
            mf.write(f"| {title_md} | {authors_md} | {year_md} | {pdf_link} |\n")
    print("Done. Index written to", INDEX_PATH)
    print("README written to", README_PATH)

if __name__ == "__main__":
    main()
