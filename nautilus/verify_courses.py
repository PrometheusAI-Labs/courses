#!/usr/bin/env python3
"""Static integrity checks for the assembled 20-hour course suite."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FORBIDDEN = re.compile(r"<(?:html|head|body|style|script)(?:\s|>)", re.I)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((ROOT / "course-manifest.json").read_text())
    docs_manifest = json.loads((ROOT / "docs-manifest.json").read_text())
    calculated_total = 0
    canonical_css = digest(ROOT / "courses" / "01-engine-foundations" / "styles.css")
    canonical_js = digest(ROOT / "courses" / "01-engine-foundations" / "main.js")

    required_release_files = (
        "index.html", "courses/index.html", "courses/resources.html", "LABS.md",
        "LEARNER_WORKBOOK.md", "INSTRUCTOR_ANSWER_KEY.md", "CAPSTONE.md",
        "PILOT_TIMING_RECORD.md", "BROWSER_ACCESSIBILITY_QA.md", "RELEASE_CANDIDATE_STATUS.md",
        "docs-manifest.json", "build_docs.py", "courses/docs/index.html", "courses/docs/docs.css",
        "THIRD_PARTY_NOTICES.md", "LICENSE.md", "LICENSES/nautilus-trader-LGPL-3.0.txt",
    )
    for relative in required_release_files:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing release file: {relative}")

    root_index = (ROOT / "index.html").read_text()
    if "courses/index.html" not in root_index:
        fail(errors, "root index.html does not route to courses/index.html")

    for course in manifest["courses"]:
        course_dir = ROOT / "courses" / course["id"]
        module_files = sorted((course_dir / "modules").glob("*.html"))
        expected_modules = course["modules"]
        expected_minutes = sum(item["minutes"] for item in expected_modules)
        calculated_total += expected_minutes

        if expected_minutes != course["minutes"]:
            fail(errors, f"{course['id']}: module minutes do not equal course minutes")
        if len(module_files) != len(expected_modules):
            fail(errors, f"{course['id']}: expected {len(expected_modules)} modules, found {len(module_files)}")

        if digest(course_dir / "styles.css") != canonical_css:
            fail(errors, f"{course['id']}: styles.css differs from the shared accessible course stylesheet")
        if digest(course_dir / "main.js") != canonical_js:
            fail(errors, f"{course['id']}: main.js differs from the shared localized course runtime")

        base = (course_dir / "_base.html").read_text()
        if '<html lang="ru">' not in base:
            fail(errors, f"{course['id']}: document language is not Russian")
        if "fonts.googleapis.com" in base or "fonts.gstatic.com" in base:
            fail(errors, f"{course['id']}: external font dependency remains")
        nav_buttons = [
            tag for tag in re.findall(r'<button class="nav-dot"[^>]*>', base)
            if "MODULE_" not in tag
        ]
        if len(nav_buttons) != len(expected_modules):
            fail(errors, f"{course['id']}: nav-dot count does not match module count")

        has_chat = False
        has_flow = False
        quiz_ids: set[str] = set()

        for expected, path in zip(expected_modules, module_files, strict=False):
            html = path.read_text()
            module_id = expected["id"]
            if FORBIDDEN.search(html):
                fail(errors, f"{path}: contains forbidden document-level tags")
            if not re.match(rf"\s*<section class=\"module\" id=\"module-{module_id}\">", html):
                fail(errors, f"{path}: wrong or missing root section")

            screens = len(re.findall(r'class="screen"', html))
            if not 3 <= screens <= 6:
                fail(errors, f"{path}: expected 3-6 screens, found {screens}")
            if html.count('class="translation-block') != 1:
                fail(errors, f"{path}: expected exactly one translation block")
            questions = html.count('class="quiz-question-block')
            if not 3 <= questions <= 5:
                fail(errors, f"{path}: expected 3-5 quiz questions, found {questions}")
            if 'class="term"' not in html:
                fail(errors, f"{path}: missing glossary terms")

            has_chat |= bool(re.search(r'class="[^"]*\bchat-window\b', html))
            has_flow |= 'class="flow-animation' in html

            for quiz_id in re.findall(r'class="quiz-container[^\"]*" id="([^"]+)"', html):
                if quiz_id in quiz_ids:
                    fail(errors, f"{path}: duplicate quiz id {quiz_id}")
                quiz_ids.add(quiz_id)

            for block in re.findall(r'<div class="quiz-question-block".*?</div>\s*</div>', html, re.S):
                correct_match = re.search(r'data-correct="([^"]+)"', block)
                values = set(re.findall(r'data-value="([^"]+)"', block))
                if correct_match and correct_match.group(1) not in values:
                    fail(errors, f"{path}: correct quiz key is absent from options")

            for steps in re.findall(r"data-steps='([^']+)'", html, re.S):
                try:
                    json.loads(steps)
                except json.JSONDecodeError as exc:
                    fail(errors, f"{path}: invalid data-steps JSON: {exc}")

        if not has_chat:
            fail(errors, f"{course['id']}: missing group chat animation")
        if not has_flow:
            fail(errors, f"{course['id']}: missing message/data flow animation")

        assembled = (course_dir / "index.html").read_text()
        expected_assembled = (course_dir / "_base.html").read_text() + "".join(
            path.read_text() for path in module_files
        ) + (course_dir / "_footer.html").read_text()
        if assembled != expected_assembled:
            fail(errors, f"{course['id']}: assembled index is stale; run build.sh")
        for expected in expected_modules:
            if f'id="module-{expected["id"]}"' not in assembled:
                fail(errors, f"{course['id']}: assembled index is missing module {expected['id']}")

    if calculated_total != manifest["total_minutes"] or calculated_total != 1200:
        fail(errors, f"Total duration must be 1200 minutes, got {calculated_total}")

    runtime = (ROOT / "courses" / "01-engine-foundations" / "main.js").read_text()
    # Match complete learner-facing phrases only. Internal JavaScript identifiers
    # such as `messages` are implementation details, not untranslated UI.
    for forbidden_english in (
        "Pick an answer first!",
        "Exactly!",
        "Not quite.",
        "Play messages",
        "Replay messages",
        "Step ",
    ):
        if forbidden_english in runtime:
            fail(errors, f"learner runtime still contains English UI: {forbidden_english!r}")
    for accessibility_marker in ("aria-pressed", "aria-selected", "tabIndex = 0", "prefers-reduced-motion"):
        corpus = runtime + (ROOT / "courses" / "01-engine-foundations" / "styles.css").read_text()
        if accessibility_marker not in corpus:
            fail(errors, f"missing accessibility marker: {accessibility_marker}")

    labs = (ROOT / "LABS.md").read_text()
    workbook = (ROOT / "LEARNER_WORKBOOK.md").read_text()
    if len(re.findall(r"^## [123]\.\d ", labs, re.M)) != 12:
        fail(errors, "LABS.md must contain 12 numbered labs")
    if len(re.findall(r"^## Артефакт [123]\.\d ", workbook, re.M)) != 12:
        fail(errors, "LEARNER_WORKBOOK.md must contain 12 numbered artifacts")

    docs_dir = ROOT / "courses" / "docs"
    expected_doc_outputs: set[str] = set()
    for item in docs_manifest["documents"]:
        source = ROOT / item["source"]
        output = docs_dir / item["output"]
        expected_doc_outputs.add(item["output"])
        if not source.is_file():
            fail(errors, f"document source is missing: {item['source']}")
            continue
        if not output.is_file():
            fail(errors, f"rendered document is missing: courses/docs/{item['output']}")
            continue
        rendered = output.read_text()
        source_hash = digest(source)
        if f'<meta name="source-sha256" content="{source_hash}">' not in rendered:
            fail(errors, f"rendered document is stale: courses/docs/{item['output']}; run build_docs.py")
        if '<html lang="ru">' not in rendered:
            fail(errors, f"rendered document language is not Russian: courses/docs/{item['output']}")
        if len(re.findall(r"<h1(?:\s|>)", rendered)) != 1:
            fail(errors, f"rendered document must contain exactly one H1: courses/docs/{item['output']}")

    docs_index = docs_dir / "index.html"
    if docs_index.is_file():
        index_html = docs_index.read_text()
        manifest_hash = digest(ROOT / "docs-manifest.json")
        if f'<meta name="docs-manifest-sha256" content="{manifest_hash}">' not in index_html:
            fail(errors, "document index is stale; run build_docs.py")
    generated_outputs = {path.name for path in docs_dir.glob("*.html")} - {"index.html", "template.html"}
    if generated_outputs != expected_doc_outputs:
        missing = sorted(expected_doc_outputs - generated_outputs)
        extra = sorted(generated_outputs - expected_doc_outputs)
        if missing:
            fail(errors, f"document outputs missing from courses/docs: {', '.join(missing)}")
        if extra:
            fail(errors, f"unmanaged document outputs in courses/docs: {', '.join(extra)}")

    pages = [ROOT / "index.html", ROOT / "courses" / "index.html", ROOT / "courses" / "resources.html"]
    pages.extend(ROOT.glob("courses/*/index.html"))
    pages.extend(path for path in ROOT.glob("courses/docs/*.html") if path.name != "template.html")
    for page in pages:
        text = page.read_text()
        ids = re.findall(r'\bid="([^"]+)"', text)
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        if duplicates:
            fail(errors, f"{page}: duplicate HTML ids: {', '.join(duplicates)}")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (page.parent / href.split("#", 1)[0]).resolve()
            if not target.exists():
                fail(errors, f"{page}: broken local link {href}")

    learner_pages = [
        ROOT / "courses" / "index.html",
        ROOT / "courses" / "resources.html",
        ROOT / "courses" / "docs" / "index.html",
    ]
    learner_pages.extend(ROOT.glob("courses/*/index.html"))
    learner_headings = "\n".join(
        " ".join(re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", page.read_text(), re.S))
        for page in learner_pages
    )
    for stale_heading in (
        "Guided lab",
        "Практикум: 12 лабораторий",
        "Документы без сырого Markdown",
        "Answer key и mastery policy",
        "Rust-first путь к live",
    ):
        if stale_heading in learner_headings:
            fail(errors, f"learner-facing heading still uses superseded wording: {stale_heading!r}")

    junk_patterns = (".DS_Store", "*.pyc", "*.swp")
    for pattern in junk_patterns:
        for path in ROOT.rglob(pattern):
            fail(errors, f"release junk present: {path.relative_to(ROOT)}")
    for dirname in ("__pycache__", ".pytest_cache"):
        for path in ROOT.rglob(dirname):
            if path.is_dir():
                fail(errors, f"release cache directory present: {path.relative_to(ROOT)}")

    if errors:
        print("COURSE VERIFICATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("COURSE VERIFICATION PASSED")
    print(f"courses={len(manifest['courses'])} modules={sum(len(c['modules']) for c in manifest['courses'])} total_minutes={calculated_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
