import os
import glob
import re

AD_CODE_1 = '''<!-- 🥇 Auto Ad #1: Display Ad -->
<div style="margin: 25px 0; text-align: center; min-height: 90px;">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2007612527496766"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-2007612527496766"
     data-ad-slot="8106603184"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>'''

AD_CODE_2 = '''<!-- 🥈 Auto Ad #2: In-Article Ad -->
<div style="margin: 25px 0; text-align: center; min-height: 90px;">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2007612527496766"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2007612527496766"
     data-ad-slot="8431552185"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
</div>'''

ROOT_FOLDER = r"C:\Users\abdul\OneDrive\Desktop\Techvibe-Web"

SKIP_FILES = ['index.html', 'about.html', 'contact.html', 'tech.html', 
              'latest-news.html', 'privacy.html', 'terms.html', 'dmca.html',
              'privac.html', 'disclaimer.html', 'editorial.html',
              'author-sarah-mitchell.html', 'google4a7fcf673558b847.html']

def insert_ads_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pehle se ad hai to skip
        if 'data-ad-slot="8106603184"' in content:
            print(f"  ⏭️  Already has ads: {os.path.basename(filepath)}")
            return False
        
        # Check: article page hai? (article-body class dhundho)
        if '<div class="article-body">' not in content:
            return False
        
        modified = False
        
        # 🥇 Ad #1: <div class="article-body"> se pehle
        content = content.replace(
            '<div class="article-body">',
            AD_CODE_1 + '\n<div class="article-body">',
            1
        )
        modified = True
        
        # 🥈 Ad #2: 4th paragraph ke baad
        paragraphs = list(re.finditer(r'<p>.*?</p>', content, re.DOTALL))
        if len(paragraphs) >= 4:
            fourth = paragraphs[3]
            insert_pos = fourth.end()
            content = content[:insert_pos] + '\n' + AD_CODE_2 + '\n' + content[insert_pos:]
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Ads inserted: {os.path.basename(filepath)}")
            return True
        
        return False
            
    except Exception as e:
        print(f"  ❌ Error in {os.path.basename(filepath)}: {e}")
        return False

print("🚀 Scanning HTML files and inserting AdSense ads...\n")

# Sirf articles folder scan karo
articles_folder = os.path.join(ROOT_FOLDER, 'articles')
html_files = glob.glob(os.path.join(articles_folder, '*.html'))
count = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    if insert_ads_in_file(filepath):
        count += 1

print(f"\n🎉 Done! Ads inserted in {count} files.")