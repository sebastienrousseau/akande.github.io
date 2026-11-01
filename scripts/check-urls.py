#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Fail when the built site points search engines at the wrong address.

Checks the output folder that Pages publishes:

- every page's canonical link is on the site's own host, never a
  development address such as http://127.0.0.1:8000;
- sitemap.xml lists only pages that exist, are indexable, and name
  themselves as canonical;
- no sitemap or feed mentions a development address;
- every address in scripts/redirects.py forwards to a page that exists;
- CNAME holds the bare host, not a DNS zone line.

    python3 scripts/check-urls.py docs
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import redirects
import sitemap

ROOT = Path(__file__).resolve().parent.parent
DEV_HOST = re.compile(r"(?:127\.0\.0\.1|localhost)(?::\d+)?")
CANONICAL = re.compile(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', re.IGNORECASE)
NOINDEX = re.compile(
    r'<meta[^>]*name="robots"[^>]*content="[^"]*noindex', re.IGNORECASE
)
LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
FEEDS = ("sitemap.xml", "news-sitemap.xml", "rss.xml", "atom.xml", "feed.json")


def page_for(out: Path, url: str, base: str) -> Path:
    """Map an absolute site URL to the file that serves it."""
    rel = url[len(base) :].lstrip("/")
    if rel == "" or rel.endswith("/"):
        return out / rel / "index.html"
    return out / rel


def check_canonicals(out: Path, base: str, skip: set) -> list:
    errors = []
    for page in sorted(out.rglob("*.html")):
        rel = page.relative_to(out)
        if rel.parts[0] in skip:
            continue
        match = CANONICAL.search(page.read_text(errors="ignore"))
        if match and not match.group(1).startswith(base + "/"):
            errors.append(f"{rel}: canonical {match.group(1)} is off-site")
    return errors


def check_feeds(out: Path) -> list:
    errors = []
    for name in FEEDS:
        feed = out / name
        if feed.is_file() and DEV_HOST.search(feed.read_text(errors="ignore")):
            errors.append(f"{name}: names a development address")
    return errors


def check_sitemap_entry(out: Path, base: str, url: str) -> str:
    """Return the problem with one sitemap URL, or an empty string."""
    if not url.startswith(base + "/"):
        return f"sitemap.xml: {url} is off-site"
    page = page_for(out, url, base)
    if not page.is_file():
        return f"sitemap.xml: {url} has no page"
    text = page.read_text(errors="ignore")
    if NOINDEX.search(text):
        return f"sitemap.xml: {url} is noindex"
    match = CANONICAL.search(text)
    if match and match.group(1) != url:
        return f"sitemap.xml: {url} declares canonical {match.group(1)}"
    return ""


def check_sitemap(out: Path, base: str) -> list:
    sitemap_file = out / "sitemap.xml"
    if not sitemap_file.is_file():
        return ["sitemap.xml: missing"]
    urls = LOC.findall(sitemap_file.read_text(errors="ignore"))
    problems = [check_sitemap_entry(out, base, url) for url in urls]
    missing = sorted(set(sitemap.listable(out, base)) - set(urls))
    problems += [f"sitemap.xml: {url} is indexable but not listed" for url in missing]
    if not urls:
        problems.append("sitemap.xml: lists no pages")
    return [p for p in problems if p]


def check_cname(out: Path, base: str) -> list:
    """CNAME, when present, must be the bare host Pages serves."""
    cname = out / "CNAME"
    host = base.split("://", 1)[-1]
    if cname.is_file() and cname.read_text().strip() != host:
        return [f"CNAME: expected {host!r}, got {cname.read_text().strip()!r}"]
    return []


def check_redirects(out: Path, redirects: dict) -> list:
    errors = []
    for old, target in redirects.items():
        page = out / old / "index.html"
        want = f'content="0; url=/{target}/"'
        if not page.is_file() or want not in page.read_text(errors="ignore"):
            errors.append(f"/{old}/ does not forward to /{target}/")
        if not (out / target / "index.html").is_file():
            errors.append(f"/{target}/ (redirect target) was not built")
    return errors


def run(out: Path) -> list:
    base = redirects.base_url(ROOT / "ssg.toml")
    return (
        check_canonicals(out, base, skip={"api"})
        + check_feeds(out)
        + check_sitemap(out, base)
        + check_redirects(out, redirects.REDIRECTS)
        + check_cname(out, base)
    )


def main(argv: list) -> int:
    out = Path(argv[0] if argv else "docs")
    errors = run(out)
    for error in errors:
        print(f"check-urls: {error}", file=sys.stderr)
    if errors:
        print(f"check-urls: {len(errors)} problem(s) in {out}", file=sys.stderr)
        return 1
    print(f"check-urls: {out} is clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
