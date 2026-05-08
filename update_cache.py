"""
update_cache.py v4.0 - ULTIMATE CACHE BUSTER + AI DETECTOR 🚀🤖
----------------------------------------------------------------
1. Saari HTML files mein CSS/JS version bump + anti-cache meta tags
2. Articles mein AI-generated content detect karta hai
3. Browser ki purani files ko forcefully clear karta hai

🎯 USAGE:
    python update_cache.py

🔴 Jab bhi CSS/JS change ho, bas NEW_VERSION number badha do!
"""

import os
import glob
import re
from datetime import datetime
from bs4 import BeautifulSoup

# ═══════════════════════════════════════════════════════════════
# 🔴 BAS YEH NUMBER BADLEIN (e.g., 5.0, 6.0, 7.0)
# ═══════════════════════════════════════════════════════════════
NEW_VERSION = "5.0"

# ═══════════════════════════════════════════════════════════════
# 🛡️ ANTI-CACHE META TAGS
# ═══════════════════════════════════════════════════════════════
CACHE_TAGS = """    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="cache-control" content="no-cache, no-store, must-revalidate">
    <meta name="expires" content="0">
    <meta name="pragma" content="no-cache">"""

# ═══════════════════════════════════════════════════════════════
# 🤖 AI DETECTION PATTERNS (Common AI writing indicators)
# ═══════════════════════════════════════════════════════════════
AI_PATTERNS = [
    # Common AI phrases
    r'\b(as an AI|I\'m an AI|as a language model|I cannot|I don\'t have personal|I apologize)\b',
    r'\b(delve into|it\'s important to note|it\'s worth noting|dive deep|in conclusion)\b',
    r'\b(in today\'s digital age|in this modern era|revolutionize|game-changer)\b',
    r'\b(foster|leverage|robust|comprehensive|multifaceted|plethora)\b',
    r'\b(navigate the landscape|paradigm shift|holistic approach|cutting-edge)\b',
    
    # Repetitive structures
    r'(firstly.*secondly.*thirdly|first and foremost|last but not least)',
    
    # Over-formal tone
    r'\b(moreover|furthermore|nevertheless|nonetheless|consequently)\b.*\b(moreover|furthermore|nevertheless|nonetheless|consequently)\b',
    
    # Generic conclusions
    r'\b(in summary|to summarize|in a nutshell|at the end of the day)\b',
]

# ═══════════════════════════════════════════════════════════════
# 🔍 AI CONTENT DETECTOR FUNCTION
# ═══════════════════════════════════════════════════════════════
def detect_ai_content(html_content, file_path):
    """
    HTML content ko parse kar ke AI patterns detect karta hai
    Returns: (is_suspicious, warnings_list)
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Article ka main content nikalo
        article_content = ""
        
        # Common article containers check karo
        main_content = (
            soup.find('article') or 
            soup.find('main') or 
            soup.find(class_=re.compile('content|article|post', re.I)) or
            soup.find('body')
        )
        
        if main_content:
            article_content = main_content.get_text()
        else:
            article_content = soup.get_text()
        
        # Normalize text
        article_content = article_content.lower()
        
        # AI patterns check karo
        warnings = []
        ai_score = 0
        
        for pattern in AI_PATTERNS:
            matches = re.findall(pattern, article_content, re.IGNORECASE)
            if matches:
                ai_score += len(matches)
                warnings.append(f"   ⚠️  Found AI phrase: '{matches[0][:50]}...'")
        
        # Word count check (AI usually writes longer, repetitive content)
        word_count = len(article_content.split())
        
        # Sentence structure analysis
        sentences = re.split(r'[.!?]+', article_content)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # AI detection threshold
        is_suspicious = False
        
        if ai_score >= 3:
            warnings.append(f"   🚨 HIGH AI SCORE: {ai_score} suspicious patterns found!")
            is_suspicious = True
        elif ai_score >= 1:
            warnings.append(f"   ⚠️  MODERATE AI SCORE: {ai_score} patterns found")
            is_suspicious = True
        
        # Overly long sentences (AI trait)
        if avg_sentence_length > 25:
            warnings.append(f"   📝 Very long sentences (avg: {avg_sentence_length:.1f} words)")
            is_suspicious = True
        
        return is_suspicious, warnings
        
    except Exception as e:
        return False, [f"   ❌ Error analyzing: {e}"]

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
print(f"🔥 CACHE BUSTER + AI DETECTOR v4.0 - Version {NEW_VERSION}")
print("=" * 70)
print(f"📁 Total Files Found: {len(html_files)}")
print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

updated_count = 0
error_count = 0
ai_detected_files = []

for file_path in html_files:
    try:
        # File read karo
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # ─────────────────────────────────────────────────────────
        # 🤖 AI CONTENT DETECTION (Articles folder ke liye)
        # ─────────────────────────────────────────────────────────
        if "article" in file_path.lower():
            is_ai, warnings = detect_ai_content(content, file_path)
            if is_ai:
                ai_detected_files.append({
                    'file': file_path,
                    'warnings': warnings
                })
        
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
        # 3️⃣ PURANE META TAGS REMOVE KARO
        # ─────────────────────────────────────────────────────────
        content = re.sub(
            r'<meta\s+http-equiv=["\']Cache-Control["\'].*?>\s*',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<meta\s+http-equiv=["\']Pragma["\'].*?>\s*',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<meta\s+http-equiv=["\']Expires["\'].*?>\s*',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r'<meta\s+name=["\']cache-control["\'].*?>\s*',
            '',
            content,
            flags=re.IGNORECASE
        )
        
        # ─────────────────────────────────────────────────────────
        # 4️⃣ NAYE META TAGS INJECT KARO
        # ─────────────────────────────────────────────────────────
        if "</head>" in content:
            content = content.replace("</head>", f"{CACHE_TAGS}\n</head>", 1)
        
        # ─────────────────────────────────────────────────────────
        # 5️⃣ FILE SAVE KARO
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

# ═══════════════════════════════════════════════════════════════
# 🤖 AI DETECTION REPORT
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("🤖 AI CONTENT DETECTION REPORT")
print("=" * 70)

if ai_detected_files:
    print(f"🚨 SUSPICIOUS AI CONTENT FOUND in {len(ai_detected_files)} files:\n")
    
    for item in ai_detected_files:
        print(f"📄 {item['file']}")
        for warning in item['warnings']:
            print(warning)
        print()
    
    print("⚠️  WARNING: In files ko manually check karein!")
    print("💡 TIP: Human-written content zyada natural aur conversational hota hai")
else:
    print("✅ No AI-generated content detected!")
    print("👍 Sab articles human-written lagte hain")

print("=" * 70)

if updated_count > 0:
    print("\n🎉 Cache successfully cleared!")
    print("🚀 Ab GitHub Desktop se Push kar sakte hain!")
else:
    print("\n⚠️  Koi file update nahi hui")

print("\n💡 TIPS:")
print("   • Browser mein Ctrl+Shift+R press kar ke hard refresh karein")
print("   • AI detected files ko manually review karein")
print("   • Human touch add karne ke liye content edit karein")