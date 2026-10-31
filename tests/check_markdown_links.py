#!/usr/bin/env python3
"""Valida referências locais em arquivos Markdown."""

from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PADRAO = re.compile(r'!?\[[^\]]*\]\(([^)\n]+)\)')

erros = []
total = 0

for markdown in sorted(ROOT.rglob("*.md")):
    if ".git" in markdown.parts:
        continue

    conteudo = markdown.read_text(encoding="utf-8")

    for referencia in PADRAO.findall(conteudo):
        destino = referencia.strip().split(" ", 1)[0]
        url = urlsplit(destino)

        if url.scheme or url.netloc or not url.path:
            continue

        total += 1
        caminho = markdown.parent / unquote(url.path)

        if caminho.is_file():
            print(f"[OK] {markdown.relative_to(ROOT)} -> {destino}")
        else:
            erros.append((markdown, destino))
            print(f"[ERRO] {markdown.relative_to(ROOT)} -> {destino}")

print(f"\nReferências locais verificadas: {total}")
print(f"Erros encontrados: {len(erros)}")

sys.exit(1 if erros else 0)
