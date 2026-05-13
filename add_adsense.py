"""
add_adsense.py — Sabhi articles mein AdSense code add karo
"""

import os

ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2007612527496766" crossorigin="anonymous"></script>'

ARTICLES_FOLDER = r"C:\Users\abdul\OneDrive\Desktop\Techvibe-Web\articles"

count = 0
for filename in os.listdir(ARTICLES_FOLDER):
    if filename.endswith(".html"):
        filepath = os.path.join(ARTICLES_FOLDER, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Skip if code already exists
        if "ca-pub-2007612527496766" in content:
            continue
        
        # Insert after <head> tag
        content = content.replace("<head>", f"<head>\n{ADSENSE_CODE}")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        count += 1
        if count % 20 == 0:
            print(f"✅ {count} articles done...")

print(f"\n🎉 Done! {count} articles updated with AdSense code.")