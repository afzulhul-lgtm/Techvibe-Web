"""
make_webp.py v2.0
-----------------
Articles folder ki saari images (jpg, jpeg, png, gif, bmp, tiff, avif)
ko WebP format mein convert karta hai aur HTML + data.json mein
extension references auto-update karta hai.
"""

import os
import glob
from PIL import Image

# Folders ka rasta
ARTICLES_DIR = "articles"
JSON_FILE = os.path.join(ARTICLES_DIR, "data.json")

# Articles folder mein saari images dhoondo (including AVIF)
images = glob.glob(os.path.join(ARTICLES_DIR, "*.jpg")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.jpeg")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.png")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.gif")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.bmp")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.tiff")) + \
         glob.glob(os.path.join(ARTICLES_DIR, "*.avif"))

if not images:
    print("⚠️ Koi image nahi mili convert karne ke liye!")
else:
    print(f"🚀 {len(images)} images ko VIP WebP format mein convert kiya ja raha hai...\n")

    for img_path in images:
        try:
            # Image ko open karo (AVIF bhi support hoga agar PIL latest version hai)
            img = Image.open(img_path)
            # Naya naam banao (.webp ke sath)
            webp_path = img_path.rsplit(".", 1)[0] + ".webp"
            
            # WebP format mein save karo (80% size kam ho jayega)
            img.save(webp_path, "webp", quality=80)
            
            # Purani heavy file ko hamesha ke liye delete kar do
            os.remove(img_path)
            print(f"✅ Converted: {os.path.basename(img_path)} -> {os.path.basename(webp_path)}")
        except Exception as e:
            print(f"❌ Error in {img_path}: {e}")

# 2. Main folder aur articles folder dono ki HTML files update karo
html_files = glob.glob("*.html") + glob.glob(os.path.join(ARTICLES_DIR, "*.html"))
for html_file in html_files:
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Jahan jahan .jpg, .jpeg, .png, .avif likha hai, usay .webp kar do
        new_content = content.replace(".jpg", ".webp").replace(".jpeg", ".webp").replace(".png", ".webp").replace(".avif", ".webp")
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        pass

# 3. data.json file ko bhi update karo taake Homepage theek rahay
if os.path.exists(JSON_FILE):
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content.replace(".jpg", ".webp").replace(".jpeg", ".webp").replace(".png", ".webp").replace(".avif", ".webp")
        
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("\n✅ data.json aur saari HTML files automatic update ho gayin!")
    except Exception as e:
        print("❌ JSON update error:", e)

print("\n🎉 BOOM! Saari images compress ho gayin aur code update ho gaya!")
print("🚀 Ab GitHub Desktop se commit aur push karein!")