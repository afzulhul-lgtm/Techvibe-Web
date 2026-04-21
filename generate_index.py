"""
generate_index.py  v2.0
========================
Run this script every time you add new articles.
Reads data.json and injects static HTML article links into index.html
so that Google can index all your articles without needing JavaScript.

HOW TO RUN:
    python generate_index.py

WHAT IT DOES:
    - Reads articles/data.json
    - Injects static article links into index.html (inside #seo-articles-ul)
    - Google can now read and index all articles
    - Users still see the normal JS card layout (static list is hidden by JS)
"""

import os
import json

# ---- CHANGE THIS PATH TO MATCH YOUR COMPUTER ----
WEBSITE_ROOT = r"C:\Users\abdul\OneDrive\Desktop\Techvibe-Web"
# --------------------------------------------------

SITE_URL   = "https://techvibedetails.online"
DATA_JSON  = os.path.join(WEBSITE_ROOT, "articles", "data.json")
INDEX_HTML = os.path.join(WEBSITE_ROOT, "index.html")

# ================================================================
print("=" * 55)
print("  TechVibe generate_index.py  v2.0")
print("=" * 55)
print()

# ================================================================
# Validate paths
# ================================================================
if not os.path.exists(DATA_JSON):
    print(f"ERROR: data.json nahi mila:\n  {DATA_JSON}")
    exit(1)

if not os.path.exists(INDEX_HTML):
    print(f"ERROR: index.html nahi mila:\n  {INDEX_HTML}")
    exit(1)

# ================================================================
# Read data.json
# ================================================================
print("Reading data.json...")

with open(DATA_JSON, "r", encoding="utf-8") as f:
    try:
        articles = json.load(f)
    except Exception as e:
        print(f"ERROR: data.json parse error: {e}")
        exit(1)

articles.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
print(f"OK: {len(articles)} articles mile\n")

# ================================================================
# Build static HTML list items
# ================================================================
def esc(text):
    """HTML-safe string."""
    return (str(text)
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<",  "&lt;")
            .replace(">",  "&gt;"))

print("Building static HTML...")

items_html = ""
for art in articles:
    title   = esc(art.get("title", ""))
    fname   = art.get("filename", "").strip()
    excerpt = esc((art.get("excerpt") or "")[:120])
    date    = art.get("date", "")
    image   = art.get("image", "")

    if not fname:
        continue

    if image and not image.startswith("http"):
        image = f"articles/{image}"

    url = f"{SITE_URL}/articles/{fname}"

    items_html += f"""                <li>
                    <a href="{url}">
                        <img src="{image}" alt="{title}" loading="lazy" width="400" height="225">
                        <div>
                            <h3>{title}</h3>
                            <p>{excerpt} &mdash; <small>{date}</small></p>
                        </div>
                    </a>
                </li>\n"""

print(f"OK: {len(articles)} articles ka HTML ready\n")

# ================================================================
# Inject into index.html
# ================================================================
print("index.html update ho raha hai...")

with open(INDEX_HTML, "r", encoding="utf-8") as f:
    html = f.read()

start_marker = "<!-- ARTICLES_PLACEHOLDER -->"
end_marker   = "<!-- generate_index.py fills this automatically -->"

if start_marker not in html or end_marker not in html:
    print("ERROR: index.html mein placeholder markers nahi mile!")
    print("Make sure index.html mein yeh dono lines hain:")
    print("  <!-- ARTICLES_PLACEHOLDER -->")
    print("  <!-- generate_index.py fills this automatically -->")
    exit(1)

before   = html[:html.index(start_marker)]
after    = html[html.index(end_marker) + len(end_marker):]
new_html = (before
            + "<!-- ARTICLES_PLACEHOLDER -->\n"
            + items_html
            + "                "
            + end_marker
            + after)

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"OK: index.html updated — {len(articles)} articles injected\n")

# ================================================================
print("=" * 55)
print(f"DONE! {len(articles)} articles Google ke liye inject ho gaye.")
print("=" * 55)
print("""
Next steps:
  1. GitHub Desktop se index.html push karein
  2. Google Search Console:
     URL Inspection -> https://techvibedetails.online/
     -> "Request Indexing"
  3. Sitemaps -> sitemap.xml resubmit karein

Har baar naye articles add karne ke baad yeh script chalayein!
""")