# SPDX-License-Identifier: Apache-2.0 OR MIT
# Semantic Version: v0.0.1
.PHONY: all build audit check-urls test contrast validate compress prune clean help

all: build

help:
	@echo "Available Makefile targets:"
	@echo "  make build      - Compile static site using Rust static-site-generator"
	@echo "  make audit      - Run WCAG 2.2 AAA (Pa11y) and Master Quality Gate audits"
	@echo "  make contrast   - Verify color tokens against WCAG 2.2 AAA math ratios"
	@echo "  make validate   - Validate Markdown frontmatter schema integrity"
	@echo "  make check-urls - Check canonicals, sitemap and redirects in docs/"
	@echo "  make compress   - Pre-compress static output with Brotli, Zstd & Gzip"
	@echo "  make prune      - Deterministically delete merged local/remote branches"
	@echo "  make clean      - Remove build artifacts and temporary files"

# Build with the latest released ssg on PATH (cargo install ssg --locked).
# --config ssg.toml is explicit: built without it, ssg used its default
# base_url and every canonical link pointed at http://127.0.0.1:8000.
build:
	@command -v ssg >/dev/null 2>&1 || { echo "ssg not found: cargo install ssg --locked"; exit 1; }
	@rm -rf public docs/tags
	@ssg build --config ssg.toml
	@# ssg writes CNAME as a DNS zone line; Pages wants the bare host.
	@cp CNAME public/CNAME
	@cp -R public/* docs/ 2>/dev/null || true
	@/usr/bin/python3 scripts/redirects.py public docs
	@# ssg writes an empty <urlset> for this site; list the built pages.
	@/usr/bin/python3 scripts/sitemap.py public docs
	@/usr/bin/python3 scripts/post-build.py

audit: contrast validate
	@if pa11y-ci --version >/dev/null 2>&1; then \
		pa11y-ci --config .pa11yci; \
	fi
	@/usr/bin/python3 scripts/regression-test.py .
	@/usr/bin/python3 scripts/check-urls.py docs

contrast:
	@/usr/bin/python3 scripts/audit-contrast.py

check-urls:
	@/usr/bin/python3 scripts/check-urls.py docs

validate:
	@/usr/bin/python3 scripts/validate-frontmatter.py

compress:
	@bash scripts/compress-assets.sh public

prune:
	@bash scripts/prune-branches.sh origin

clean:
	@rm -rf public dist .cache coverage *.log
	@echo "Workspace cleaned."
