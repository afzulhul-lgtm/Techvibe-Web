"""
generate_index.py
=================
Run this script every time you add new articles.
It reads data.json and injects static HTML article links into index.html
so that Google can index all your articles without needing JavaScript.

HOW TO RUN:
    python generate_index.py

WHAT IT DOES:
    - Reads articles/data.json
    - Injects static article links into index.html (inside #seo-articles-ul)
    - Google can now read and index all 173+ articles
    - Users still see the normal JS card layout (static list is hidden by JS)
"""

import os
import json
import re

# ---- CHANGE THIS PATH TO MATCH YOUR COMPUTER ----
WEBSITE_ROOT = r"C:\Users\abdul\OneDrive\Desktop\Techvibe-Web"
# --------------------------------------------------

SITE_URL = "https://techvibedetails.online"
DATA_JSON = os.path.join(WEBSITE_ROOT, "articles", "data.json")
INDEX_HTML = os.path.join(WEBSITE_ROOT, "index.html")

print("Reading data.json...")

with open(DATA_JSON, "r", encoding="utf-8") as f:
    articles = json.load(f)

articles.sort(key=lambda x: int(x.get("id", 0)), reverse=True)
print(f"Found {len(articles)} articles")

# Build static HTML list items
items_html = ""
for art in articles:
    title   = art.get("title", "").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    fname   = art.get("filename", "")
    excerpt = (art.get("excerpt") or "")[:120].replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
    date    = art.get("date", "")
    image   = art.get("image", "")
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

print(f"Built static HTML for {len(articles)} articles")

# Read index.html
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the placeholder section
start_marker = "<!-- ARTICLES_PLACEHOLDER -->"
end_marker   = "<!-- generate_index.py fills this automatically -->"

if start_marker in html and end_marker in html:
    before = html[:html.index(start_marker)]
    after  = html[html.index(end_marker) + len(end_marker):]
    new_html = before + "<!-- ARTICLES_PLACEHOLDER -->\n" + items_html + "                " + end_marker + after
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"index.html updated — {len(articles)} articles injected for Google")
else:
    print("ERROR: Placeholder markers not found in index.html")
    print("Make sure your index.html contains:")
    print("  <!-- ARTICLES_PLACEHOLDER -->")
    print("  <!-- generate_index.py fills this automatically -->")
    exit(1)

print("""
Done!

Next steps:
  1. Upload the updated index.html to your website
  2. Go to Google Search Console
  3. URL Inspection > https://techvibedetails.online/ > Request Indexing
  4. Sitemaps > Resubmit sitemap.xml

Run this script again every time you publish new articles.
""")