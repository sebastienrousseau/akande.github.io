#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Write sitemap.xml from the pages the build produced.

ssg writes an empty <urlset> for this site, and a hand-filled sitemap in
docs/ was lost on every rebuild. This lists every page that is
indexable and names itself as canonical, skipping utility pages, dated
by the last commit so a rebuild of the same commit gives the same file.
jspassgen.github.io does the same in its post-build step.

    python3 scripts/sitemap.py public docs
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redirects import base_url

ROOT = Path(__file__).resolve().parent.parent
# Utility pages that exist but are not content.
SKIP = {"404", "offline", "thanks", "api"}
CANONICAL = re.compile(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', re.IGNORECASE)
NOINDEX = re.compile(
    r'<meta[^>]*name="robots"[^>]*content="[^"]*noindex', re.IGNORECASE
)


def last_commit_date() -> str:
    date = os.environ.get("SITE_DATE")
    if date:
        return date
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs"],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    return out.stdout.strip() or "1970-01-01"


def page_url(out: Path, page: Path, base: str) -> str:
    """The address a page's index.html is served at."""
    rel = page.parent.relative_to(out).as_posix()
    return f"{base}/" if rel == "." else f"{base}/{rel}/"


def listable(out: Path, base: str) -> list:
    """URLs of indexable pages that name themselves as canonical."""
    urls = []
    for page in sorted(out.rglob("index.html")):
        parts = page.relative_to(out).parts
        if len(parts) > 1 and parts[0] in SKIP:
            continue
        text = page.read_text(errors="ignore")
        match = CANONICAL.search(text)
        url = page_url(out, page, base)
        if match and match.group(1) == url and not NOINDEX.search(text):
            urls.append(url)
    return urls


def render(urls: list, date: str) -> str:
    body = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{date}</lastmod>\n  </url>\n"
        for u in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}</urlset>\n"
    )


def main(argv: list) -> int:
    base = base_url(ROOT / "ssg.toml")
    date = last_commit_date()
    for folder in argv or ["public"]:
        out = Path(folder)
        if not out.is_dir():
            continue
        urls = listable(out, base)
        (out / "sitemap.xml").write_text(render(urls, date), encoding="utf-8")
        print(f"sitemap: {len(urls)} page(s) in {out}/sitemap.xml, dated {date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
