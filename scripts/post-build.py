import os, re, json, hashlib, base64

repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_sri_hash(filepath):
    if not os.path.isfile(filepath): return None
    with open(filepath, "rb") as f: data = f.read()
    digest = hashlib.sha384(data).digest()
    return "sha384-" + base64.b64encode(digest).decode("ascii")

clean_navbar = '''  <!-- Responsive Navbar -->
  <nav class="navbar" aria-label="Main Navigation">
    <div class="navbar-container">
      <div class="navbar-header">
        <a class="navbar-brand" href="/" aria-label="Àkàndé Homepage">
          <img src="https://cloudcdn.pro/akande/v1/logos/akande.svg" alt="Àkàndé Logo" width="32" height="32" class="d-inline-block" />
          <span class="navbar-brand-text">Àkàndé Voice Assistant</span>
        </a>

        <!-- Mobile actions (Search + Theme + Toggle) -->
        <div class="navbar-actions d-flex d-lg-none">
          <button type="button" class="btn search-trigger" id="searchTriggerMobile" aria-label="Search">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          </button>

          <div class="theme-switcher" role="radiogroup" aria-label="Theme mode">
            <button type="button" class="theme-btn" data-theme-mode="light" aria-label="Light mode">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
            </button>
            <button type="button" class="theme-btn" data-theme-mode="dark" aria-label="Dark mode">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            </button>
            <button type="button" class="theme-btn active" data-theme-mode="system" aria-label="System mode">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
            </button>
          </div>

          <button type="button" class="navbar-toggle" id="navbarToggle" aria-expanded="false" aria-controls="navbarMenu" aria-label="Toggle navigation menu">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          </button>
        </div>
      </div>

      <!-- Links menu -->
      <div class="navbar-menu" id="navbarMenu">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="/features/index.html">Features</a></li>
          <li class="nav-item"><a class="nav-link" href="/about/index.html">About</a></li>
          <li class="nav-item nav-item-cta"><a class="btn btn-dark ms-lg-2" href="/contact/index.html">Get in touch</a></li>
        </ul>
      </div>

      <!-- Desktop actions -->
      <div class="navbar-actions d-none d-lg-flex">
        <button type="button" class="btn search-trigger" id="searchTrigger" aria-label="Search">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <span>Search</span>
          <kbd class="search-kbd">⌘K</kbd>
        </button>

        <div class="theme-switcher" role="radiogroup" aria-label="Theme mode">
          <button type="button" class="theme-btn" data-theme-mode="light" aria-label="Light mode">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
          </button>
          <button type="button" class="theme-btn" data-theme-mode="dark" aria-label="Dark mode">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          </button>
          <button type="button" class="theme-btn active" data-theme-mode="system" aria-label="System mode">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
          </button>
        </div>
      </div>
    </div>
  </nav>'''

search_modal = '''  <!-- Search Modal Dialog -->
  <div id="searchModal" class="search-modal" role="dialog" aria-modal="true" aria-label="Site Search">
    <div class="search-backdrop"></div>
    <div class="search-dialog">
      <div class="search-header">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="search" id="searchInput" class="search-input" placeholder="Search pages, articles, docs..." aria-label="Search query" autocomplete="off">
        <button type="button" class="search-close" id="searchClose" aria-label="Close search">✕</button>
      </div>
      <div id="searchResults" class="search-results" role="listbox">
        <div class="search-empty">Type to search...</div>
      </div>
    </div>
  </div>'''

# Ensure valid root main.js and styles.css exist
with open(os.path.join(repo_dir, "main.js"), "r", errors="ignore") as f:
    master_js = f.read()

with open(os.path.join(repo_dir, "styles.css"), "r", errors="ignore") as f:
    master_css = f.read()

for folder in ["public", "docs"]:
    f_dir = os.path.join(repo_dir, folder)
    if not os.path.isdir(f_dir): continue

    # Always keep valid uncorrupted main.js and styles.css
    with open(os.path.join(f_dir, "main.js"), "w", errors="ignore") as f:
        f.write(master_js)
    with open(os.path.join(f_dir, "styles.css"), "w", errors="ignore") as f:
        f.write(master_css)

    # Clean search index of utility pages
    s_index_path = os.path.join(f_dir, "search-index.json")
    if os.path.isfile(s_index_path):
        try:
            with open(s_index_path, "r") as f:
                s_data = json.load(f)
            if isinstance(s_data, dict) and "entries" in s_data:
                s_data["entries"] = [item for item in s_data["entries"] if not any(u in item.get("url", "") for u in ["404", "offline", "thanks"])]
                with open(s_index_path, "w") as f:
                    json.dump(s_data, f, indent=2)
            elif isinstance(s_data, list):
                s_data = [item for item in s_data if not any(u in item.get("url", "") for u in ["404", "offline", "thanks"])]
                with open(s_index_path, "w") as f:
                    json.dump(s_data, f, indent=2)
        except Exception:
            pass

    # Compute SRI hashes for canonical assets
    main_js_hash = get_sri_hash(os.path.join(f_dir, "main.js"))
    styles_css_hash = get_sri_hash(os.path.join(f_dir, "styles.css"))

    # Post-process all html pages
    for root, dirs, files in os.walk(f_dir):
        dirs[:] = [d for d in dirs if d not in ["_layouts", "templates", "source", "target", "node_modules", ".git", ".github", ".lighthouseci", "dashboard", "_csp"]]
        for f in files:
            if f.endswith(".html"):
                fpath = os.path.join(root, f)
                with open(fpath, "r", errors="ignore") as fp:
                    htxt = fp.read()

                # Ensure CSP has unsafe-inline
                csp_meta = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\' \'unsafe-inline\' \'unsafe-eval\' https://cdn.jsdelivr.net; connect-src \'self\' https://formspree.io; img-src \'self\' data: https: https://cloudcdn.pro; style-src \'self\' \'unsafe-inline\' https://cdn.jsdelivr.net; font-src \'self\'; form-action \'self\' https://formspree.io;" />'
                if re.search(r'<meta[^>]*http-equiv=["\']Content-Security-Policy["\'][^>]*>', htxt, re.IGNORECASE):
                    htxt = re.sub(r'<meta[^>]*http-equiv=["\']Content-Security-Policy["\'][^>]*>', csp_meta, htxt, flags=re.IGNORECASE)
                else:
                    htxt = htxt.replace('<head>', f'<head>\n  {csp_meta}')

                # 1. Remove SSG Auto-injected search elements & broken CSP scripts
                htxt = re.sub(r'<!-- SSG Search Widget -->.*', '', htxt, flags=re.DOTALL)
                htxt = re.sub(r'<div id="ssg-search-widget"[^>]*>.*?</div>\s*</div>', '', htxt, flags=re.DOTALL)
                htxt = re.sub(r'<div id="ssg-search-overlay"[^>]*>.*?</div>\s*</div>', '', htxt, flags=re.DOTALL)
                htxt = re.sub(r'<script[^>]*src="/_csp/[^"]+"[^>]*>\s*</script>', '', htxt)
                htxt = re.sub(r'<link[^>]*href="/_csp/[^"]+"[^>]*>', '', htxt)

                # 2. Strip any escaped HTML container tags completely
                htxt = re.sub(r'&lt;div\b.*?&gt;', '', htxt)
                htxt = re.sub(r'&lt;/div&gt;', '', htxt)
                htxt = re.sub(r'&lt;h([1-6])\b.*?&gt;', r'<h\1>', htxt)
                htxt = re.sub(r'&lt;/h([1-6])&gt;', r'</h\1>', htxt)
                htxt = re.sub(r'&lt;p\b.*?&gt;', '<p>', htxt)
                htxt = re.sub(r'&lt;/p&gt;', '</p>', htxt)
                htxt = re.sub(r'&lt;strong\b.*?&gt;', '<strong>', htxt)
                htxt = re.sub(r'&lt;/strong&gt;', '</strong>', htxt)
                htxt = re.sub(r'&lt;a\s+href=&quot;([^&]*)&quot;.*?&gt;', r'<a href="\1">', htxt)
                htxt = re.sub(r'&lt;/a&gt;', '</a>', htxt)
                htxt = re.sub(r'&lt;img\b.*?&gt;', '', htxt)
                htxt = re.sub(r'&lt;meta\b.*?&gt;', '', htxt)

                # 3. Fix JSON-LD description entity leaks
                def clean_json_ld(m):
                    j_txt = m.group(1)
                    j_txt = re.sub(r'&lt;.*', '', j_txt)
                    return f'<script type="application/ld+json">{j_txt}</script>'
                htxt = re.sub(r'<script type="application/ld\+json">(.*?)</script>', clean_json_ld, htxt, flags=re.DOTALL)

                # 4. Canonicalize main.js and styles.css tags
                htxt = re.sub(r'<script[^>]*src="/main(?:\.[0-9a-f]+)?\.js"[^>]*>\s*</script>', 
                              f'<script src="/main.js" integrity="{main_js_hash}" defer></script>', 
                              htxt)
                htxt = re.sub(r'<link[^>]*href="/styles(?:\.[0-9a-f]+)?\.css"[^>]*>', 
                              f'<link rel="stylesheet" href="/styles.css" integrity="{styles_css_hash}">', 
                              htxt)

                # 5. Ensure single navbar and search modal exist
                if '<nav class="navbar"' not in htxt and '<nav' not in htxt:
                    htxt = re.sub(r'<body[^>]*>', r'\g<0>\n' + clean_navbar, htxt)
                elif '<nav class="navbar"' not in htxt and '<nav' in htxt:
                    htxt = re.sub(r'<nav\b[^>]*>.*?</nav>', clean_navbar, htxt, flags=re.DOTALL)

                # 6. Ensure searchModal and script exist before closing body
                if 'id="searchModal"' not in htxt:
                    # Strip any trailing body/html tags first
                    htxt = re.sub(r'(?:</body>\s*)*(?:</html>\s*)*$', '', htxt.strip(), flags=re.IGNORECASE)
                    htxt += f'\n{search_modal}\n<script src="/main.js" integrity="{main_js_hash}" defer></script>\n</body>\n</html>\n'
                else:
                    htxt = re.sub(r'(?:</body>\s*)*(?:</html>\s*)*$', '', htxt.strip(), flags=re.IGNORECASE)
                    htxt += '\n</body>\n</html>\n'

                with open(fpath, "w", errors="ignore") as fp:
                    fp.write(htxt)

print("Post-build optimization completed with uncorrupted main.js and clean HTML closing tags.")
