#!/usr/bin/env python3
"""Render project Markdown into polished, offline HTML resource pages."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "courses" / "docs"
MANIFEST = ROOT / "docs-manifest.json"
TEMPLATE = DOCS_DIR / "template.html"

CATEGORY_TITLES = {
    "learning": "Учебные материалы",
    "teaching": "Преподавателю",
    "reference": "Источники и лицензии",
    "release": "Подготовка публикации",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linkify_known_files(markdown: str, outputs: dict[str, str]) -> str:
    """Turn inline-code references to shipped files into local web links."""
    special = {
        "course-manifest.json": "../../course-manifest.json",
    }
    links = outputs | special
    result: list[str] = []
    fenced = False
    for line in markdown.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            result.append(line)
            continue
        if not fenced:
            for label, target in links.items():
                line = line.replace(f"`{label}`", f"[`{label}`]({target})")
        result.append(line)
    return "".join(result)


def render_document(pandoc: str, item: dict[str, str], outputs: dict[str, str]) -> None:
    source = ROOT / item["source"]
    destination = DOCS_DIR / item["output"]
    source_text = source.read_text(encoding="utf-8")
    if item.get("format") == "plain":
        markdown = f'<pre class="license-text">{html.escape(source_text)}</pre>\n'
    else:
        # The page template already renders the document title as its sole H1.
        # Remove the source H1 so the visible hierarchy begins with H2 sections.
        source_without_title = re.sub(r"\A#\s+[^\n]+\n+", "", source_text, count=1)
        markdown = linkify_known_files(source_without_title, outputs)
    command = [
        pandoc,
        "--from=gfm+raw_html",
        "--to=html5",
        "--standalone",
        "--toc",
        "--toc-depth=3",
        f"--template={TEMPLATE}",
        "--metadata",
        f"title={item['title']}",
        "--metadata",
        f"description={item['summary']}",
        "--metadata",
        f"audience={item['audience']}",
        "--metadata",
        f"source_file={item['source']}",
        "--metadata",
        f"source_sha256={sha256(source)}",
    ]
    completed = subprocess.run(
        command,
        input=markdown,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or f"pandoc failed for {source}")
    rendered = re.sub(r' id="toc-[^"]+"', "", completed.stdout)
    destination.write_text(rendered, encoding="utf-8")


def render_index(documents: list[dict[str, str]]) -> None:
    groups: list[str] = []
    for category, heading in CATEGORY_TITLES.items():
        cards: list[str] = []
        for item in documents:
            if item["category"] != category:
                continue
            cards.append(
                "".join(
                    [
                        f'<a class="doc-card" href="{html.escape(item["output"])}">',
                        f'<span class="audience">{html.escape(item["audience"])}</span>',
                        f'<h3>{html.escape(item["title"])}</h3>',
                        f'<p>{html.escape(item["summary"])}</p>',
                        '<span class="open">Открыть документ →</span>',
                        "</a>",
                    ]
                )
            )
        groups.append(
            f'<section class="docs-group"><h2>{html.escape(heading)}</h2>'
            f'<div class="docs-grid">{"".join(cards)}</div></section>'
        )

    page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Удобные HTML-версии всех документов NautilusTrader Academy.">
  <meta name="docs-manifest-sha256" content="{sha256(MANIFEST)}">
  <title>Документы — NautilusTrader Academy</title>
  <link rel="stylesheet" href="docs.css">
</head>
<body>
  <a class="skip-link" href="#documents">К документам</a>
  <header class="site-header">
    <a class="brand" href="../index.html">NautilusTrader Academy</a>
    <nav aria-label="Основная навигация"><a href="../resources.html">Материалы</a><a href="../index.html">Курсы</a></nav>
  </header>
  <main class="docs-home" id="documents">
    <h1>Документы программы</h1>
    <p class="lead">Учебные, преподавательские, справочные и редакционные материалы открываются как удобные HTML-страницы с оглавлением, таблицами, печатью и понятной навигацией.</p>
    {''.join(groups)}
  </main>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(page, encoding="utf-8")


def main() -> int:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        print("ERROR: pandoc is required to rebuild document HTML", file=sys.stderr)
        return 1
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    documents = payload["documents"]
    outputs = {item["source"]: item["output"] for item in documents}
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for item in documents:
        render_document(pandoc, item, outputs)
    render_index(documents)
    print(f"Built {len(documents)} document pages and courses/docs/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
