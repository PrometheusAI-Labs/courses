#!/usr/bin/env python3
"""Verify brief and module snippets against a pinned NautilusTrader checkout."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path


PINNED_COMMIT = "84a98f7f3cc786085496976320c3cb320024217f"
ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="NautilusTrader checkout at the pinned commit")
    args = parser.parse_args()
    source = args.source.resolve()

    actual_commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    if actual_commit != PINNED_COMMIT:
        print(f"ERROR: expected {PINNED_COMMIT}, got {actual_commit}")
        return 1

    errors: list[str] = []
    briefs = sorted((ROOT / "courses").glob("*/briefs/*.md"))
    for brief in briefs:
        text = brief.read_text()
        match = re.search(
            r"File: ([^ ]+) \(lines (\d+)-(\d+), exact continuous excerpt[^\n]*\)\n```(?:python|rust)\n(.*?)\n```",
            text,
            re.S,
        )
        if not match:
            errors.append(f"{brief}: missing exact source declaration")
            continue

        relative, start_text, end_text, brief_code = match.groups()
        start, end = int(start_text), int(end_text)
        source_lines = (source / relative).read_text().splitlines()
        expected = "\n".join(source_lines[start - 1 : end])
        if brief_code != expected:
            errors.append(f"{brief}: brief snippet differs from {relative}:{start}-{end}")

        module_name = brief.name.replace(".md", ".html")
        module = brief.parents[1] / "modules" / module_name
        if not module.exists():
            errors.append(f"{module}: corresponding module missing")
            continue
        module_text = module.read_text()
        code_match = re.search(r"<pre><code>(.*?)</code></pre>", module_text, re.S)
        if not code_match:
            errors.append(f"{module}: code panel missing")
            continue
        module_code = html.unescape(re.sub(r"<[^>]+>", "", code_match.group(1))).strip("\n")
        if module_code != expected:
            errors.append(f"{module}: displayed snippet differs from pinned source")

    if errors:
        print("SOURCE SNIPPET VERIFICATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"SOURCE SNIPPET VERIFICATION PASSED: {len(briefs)} exact excerpts at {PINNED_COMMIT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
