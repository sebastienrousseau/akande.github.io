#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Keep the site's renamed addresses working.

GitHub Pages has no server-side redirect, so each old address gets a small
page that sends the visitor on: a meta refresh for browsers, a canonical
link and noindex for crawlers, and an ordinary link for anything that
follows neither. The pages are written after ssg has generated the
sitemap and feeds, so nothing lists them.

    python3 scripts/redirects.py public docs
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Old path -> path it moved to. "made-with-shokunin" was renamed to
# "made-with-ssg" in #3, and Search Console still reports the old one.
REDIRECTS = {
    "made-with-shokunin": "made-with-ssg",
}

PAGE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="refresh" content="0; url=/{target}/" />
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{base}/{target}/" />
  <title>This page has moved</title>
</head>
<body>
  <main id="main">
    <h1>This page has moved</h1>
    <p>It now lives at <a href="/{target}/">{host}/{target}/</a>.</p>
  </main>
</body>
</html>
"""


def base_url(config: Path) -> str:
    """Return base_url from ssg.toml, the site's single source for it."""
    match = re.search(r'^base_url\s*=\s*"([^"]+)"', config.read_text(), re.MULTILINE)
    if not match:
        raise SystemExit(f"redirects: no base_url in {config}")
    return match.group(1).rstrip("/")


def write_redirects(out: Path, base: str) -> None:
    """Write one redirect page per entry in REDIRECTS under out."""
    host = base.split("://", 1)[-1]
    for old, target in REDIRECTS.items():
        if not (out / target / "index.html").is_file():
            raise SystemExit(f"redirects: target /{target}/ missing in {out}")
        page = out / old / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            PAGE.format(base=base, host=host, target=target), encoding="utf-8"
        )


def main(argv: list[str]) -> int:
    base = base_url(Path(__file__).resolve().parent.parent / "ssg.toml")
    for folder in argv or ["public"]:
        out = Path(folder)
        if out.is_dir():
            write_redirects(out, base)
            print(f"redirects: {len(REDIRECTS)} old address(es) in {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
