#!/usr/bin/env python3
"""Quét slides/ và demos/, đọc <title> (và <meta name="description">) của từng file HTML,
rồi ghi ra manifest.js cho trang chủ. Chạy: python3 scripts/build_manifest.py"""
import html, json, re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = {"slides": "slides", "demos": "demos"}

def read_head(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(200_000)  # head nằm ở đầu file, tránh đọc cả file nặng

def meta(path):
    head = read_head(path)
    t = re.search(r"<title[^>]*>(.*?)</title>", head, re.I | re.S)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', head, re.I | re.S)
    title = html.unescape(t.group(1)).strip() if t else ""
    return (title or path.stem.replace("_", " ")), (html.unescape(d.group(1)).strip() if d else "")

items = []
for kind, folder in SECTIONS.items():
    for p in sorted((ROOT / folder).glob("*.html")):
        title, desc = meta(p)
        items.append({
            "type": kind,
            "title": title,
            "description": desc,
            "url": f"{folder}/{quote(p.name)}",
        })

(ROOT / "manifest.js").write_text(
    "window.ITEMS = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
print(f"manifest.js: {len(items)} mục")
