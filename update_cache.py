import os
import glob
import re

# 🔴 Jab bhi aap mustaqbil (future) mein koi Design/JS change karein, toh bas is number ko badal dein (e.g., 5.0, 6.0)
NEW_VERSION = "4.0"

# Anti-Cache Tags (Jo browser ko purani file save karne se rokte hain)
CACHE_TAGS = """
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
"""

# Current folder aur articles folder dono ki HTML files uthao
html_files = glob.glob("*.html") + glob.glob("articles/*.html")

print(f"🔄 Total {len(html_files)} files update ho rahi hain (Version {NEW_VERSION})...")

for file_path in html_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. CSS aur JS ka version update karo
        content = re.sub(r'style\.css\?v=[\d\.]+', f'style.css?v={NEW_VERSION}', content)
        content = re.sub(r'script\.js\?v=[\d\.]+', f'script.js?v={NEW_VERSION}', content)

        # 2. Agar Meta Tags nahi lage toh laga do
        if "Cache-Control" not in content and "</head>" in content:
            content = content.replace("</head>", f"{CACHE_TAGS}\n</head>")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")

print("✅ VIP Cache System saari files mein lag gaya hai! 🔥")
print("✅ Ab aap apna code GitHub Desktop se Push kar sakte hain.")