"""
update_cache.py v5.1 - SMART CACHE BUSTER (No Duplicates)
-----------------------------------------------------------
1. CSS/JS version bump karta hai
2. Anti-cache meta tags inject karta hai (sirf agar pehle se na ho)
3. Duplicate meta tags nahi banata

🎯 USAGE:
    python update_cache.py

🔴 Jab bhi CSS/JS change ho, bas NEW_VERSION number badha do!
"""

import os
import glob
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 🔴 BAS YEH NUMBER BADLEIN
# ═══════════════════════════════════════════════════════════════
NEW_VERSION = "5.0"

# ═══════════════════════════════════════════════════════════════
# 🛡️ ANTI-CACHE META TAGS (sirf ye do jo hamesha add hote the)
# ═══════════════════════════════════════════════════════════════
META_EXPIRES = '<meta name="expires" content="0">'
META_PRAGMA  = '<meta name="pragma" content="no-cache">'

# ═══════════════════════════════════════════════════════════════
# 📂 HTML FILES COLLECT KARO
# ═══════════════════════════════════════════════════════════════
html_files = []
html_files.extend(glob.glob("*.html"))
html_files.extend(glob.glob("articles/*.html"))
html_files.extend(glob.glob("**/*.html", recursive=True))
html_files = list(set(html_files))

# ═══════════════════════════════════════════════════════════════
# 🚀 PROCESSING START
# ═══════════════════════════════════════════════════════════════
print("=" * 70)
print(f"🔥 SMART CACHE BUSTER v5.1 - Version {NEW_VERSION}")
print("=" * 70)
print(f"📁 Total Files Found: {len(html_files)}")
print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

updated_count = 0
error_count = 0

for file_path in html_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # ─────────────────────────────────────────────────────────
        # 1️⃣ CSS VERSION UPDATE
        # ─────────────────────────────────────────────────────────
        content = re.sub(
            r'(href=["\'](?:\.\.\/)?style\.css)\?v=[\d\.]+',
            rf'\1?v={NEW_VERSION}',
            content
        )
        content = re.sub(
            r'(href=["\'](?:\.\.\/)?style\.css)(["\'])',
            rf'\1?v={NEW_VERSION}\2',
            content
        )
        
        # ─────────────────────────────────────────────────────────
        # 2️⃣ JS VERSION UPDATE
        # ─────────────────────────────────────────────────────────
        content = re.sub(
            r'(src=["\'](?:\.\.\/)?script\.js)\?v=[\d\.]+',
            rf'\1?v={NEW_VERSION}',
            content
        )
        content = re.sub(
            r'(src=["\'](?:\.\.\/)?script\.js)(["\'])',
            rf'\1?v={NEW_VERSION}\2',
            content
        )
        
        # ─────────────────────────────────────────────────────────
        # 3️⃣ ANTI-CACHE META TAGS — sirf agar pehle se na ho
        # ─────────────────────────────────────────────────────────
        if META_EXPIRES not in content:
            if "</head>" in content:
                content = content.replace("</head>", f"    {META_EXPIRES}\n</head>", 1)
        
        if META_PRAGMA not in content:
            if "</head>" in content:
                content = content.replace("</head>", f"    {META_PRAGMA}\n</head>", 1)
        
        # ─────────────────────────────────────────────────────────
        # 4️⃣ FILE SAVE KARO
        # ─────────────────────────────────────────────────────────
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ {file_path}")
            updated_count += 1
        else:
            print(f"⏭️  {file_path} (No changes needed)")
            
    except Exception as e:
        print(f"❌ ERROR in {file_path}: {e}")
        error_count += 1

# ═══════════════════════════════════════════════════════════════
# 📊 FINAL REPORT
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("📊 CACHE UPDATE REPORT")
print("=" * 70)
print(f"✅ Updated: {updated_count} files")
print(f"❌ Errors: {error_count} files")
print(f"📁 Total: {len(html_files)} files")
print(f"🔢 New Version: {NEW_VERSION}")

if updated_count > 0:
    print("\n🎉 Cache successfully cleared!")
    print("🚀 Ab GitHub Desktop se Push kar sakte hain!")
else:
    print("\n⚠️  Koi file update nahi hui")

print("\n💡 TIPS:")
print("   • Browser mein Ctrl+Shift+R press kar ke hard refresh karein")
print("=" * 70)