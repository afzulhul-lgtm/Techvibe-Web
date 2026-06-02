import os
import glob
import re
from datetime import datetime
from xml.etree import ElementTree as ET

# ============================================================
#   SPAM ARTICLES CLEANUP SCRIPT
#   techvibedetails.online
#   Run: python cleanup_spam_articles.py
# ============================================================

# ✅ Apna articles folder ka path yahan set karo
ARTICLES_FOLDER = "articles"       # articles/ folder
SITEMAP_FILE    = "sitemap.xml"    # root mein sitemap.xml
SITE_URL        = "https://techvibedetails.online"

# ============================================================
#  SPAM ARTICLE FILENAMES — ye sab DELETE honge
#  (URL se .html extension wali files)
# ============================================================

SPAM_FILES = [

    # ❌ FAKE PAYMENT / FINANCE ARTICLES
    "confirmed-federal-2000-direct-deposit-coming-february-2026-what-you-mu-62.html",
    "urgent-alert-federal-2000-payments-arriving-in-february-2026-ultimate-59.html",
    "shocking-2026-social-security-update-why-your-payment-dates-are-now-co-63.html",
    "february-2026-social-security-ssi-payment-dates-officially-confirmed-f-67.html",
    "massive-relief-how-to-claim-your-federal-2000-payment-in-february-2026-68.html",
    "1000-to-2000-irs-refunds-confirmed-for-2026-check-eligibility-exact-ti-69.html",
    "critical-snap-update-usda-announces-strict-new-work-rules-starting-feb-30.html",
    "1000-baby-benefit-announced-everything-parents-need-to-know-about-the-31.html",
    "social-security-alert-massive-changes-to-your-february-2026-ssi-checks-32.html",
    "irs-urgent-warning-2026-160-million-lost-to-social-media-tax-scams-are-172.html",

    # ❌ FAKE WEATHER / EMERGENCY ARTICLES
    "officially-confirmed-devastating-heavy-snow-begins-tonight-major-trave-61.html",
    "severe-blizzard-warning-historic-snowfall-threatens-to-cripple-transpo-35.html",
    "winter-storm-emergency-70-mph-winds-and-3-feet-of-snow-approaching-rap-36.html",
    "urgent-warning-massive-polar-vortex-disruption-threatens-widespread-tr-81.html",
    "confirmed-a-historic-february-polar-vortex-disruption-is-coming-prepar-82.html",
    "urgent-warning-issued-bizarre-february-atmospheric-signals-threaten-ar-37.html",
    "authorities-issue-urgent-stay-home-warning-as-heavy-snow-hits-tonight-38.html",
    "businesses-refuse-to-close-as-authorities-beg-drivers-to-avoid-deadly-40.html",
    "heavy-snow-alert-authorities-urge-drivers-to-stay-home-tonight-12.html",
    "situation-critical-looming-heavy-snow-creates-chaos-between-authoritie-43.html",
    "early-february-climate-signals-why-the-arctic-is-behaving-strangely-14.html",
    "arctic-entering-uncharted-territory-meteorologists-issue-early-februar-11.html",
    "unprecedented-atmospheric-shift-polar-vortex-magnitude-reaches-histori-3.html",

    # ❌ FAKE / DUPLICATE DRIVING LAW ARTICLES
    "critical-alert-the-new-2026-driving-law-affecting-all-50-states-ignore-66.html",
    "urgent-warning-strict-new-february-2026-driving-law-could-mean-fines-j-65.html",
    "urgent-alert-for-us-drivers-the-new-february-2026-driving-law-that-cou-33.html",

    # ❌ FAKE / MISLEADING AI & TECH ARTICLES
    "gpt-56-leak-release-date-features-what-openai-isnt-telling-us.html",
    "your-bosss-tracking-software-is-secretly-sharing-your-data-with-google.html",
    "google-ai-search-backlash-users-threaten-mass-exodus-over-misinformati.html",
    "warning-hackers-are-sending-fake-jpeg-photos-that-silently-take-over-y-184.html",
    "tiny-startup-humiliates-nvidia-and-amd-runs-700b-ai-models-on-a-0-clou-183.html",
    "m5-macbook-pro-hinge-causes-sparks-and-catches-fire-just-two-days-afte-178.html",

    # ❌ SENSATIONAL / MISLEADING SCIENCE ARTICLES
    "scientists-shock-the-world-have-we-completely-miscalculated-the-earths-26.html",
    "everything-we-knew-is-wrong-dinosaurs-and-mammoths-were-shockingly-slo-34.html",
    "quantum-physics-shocker-electrons-dont-entangle-all-at-once-the-mind-b-90.html",
    "mind-blowing-science-why-sweet-potatoes-and-regular-potatoes-are-actua-84.html",
    "long-before-trees-earth-was-ruled-by-this-mysterious-giant-lifeform-9.html",

    # ❌ FAKE MEDICAL / HEALTH CLICKBAIT
    "medical-miracle-groundbreaking-strategy-finally-forces-cancer-cells-to-89.html",
    "medical-breakthrough-doctors-finally-reveal-why-you-get-leisure-migrai-83.html",
    "over-65-and-losing-flexibility-new-study-reveals-its-not-your-muscles-87.html",
    "psychologists-warn-these-9-common-parenting-mistakes-are-guaranteed-to-91.html",
    "critical-alert-vets-issue-urgent-life-saving-warning-to-all-cat-owners-85.html",

    # ❌ FAKE MILITARY / POLITICAL CLICKBAIT
    "global-alert-uss-gerald-r-ford-deployed-to-europe-as-us-prepares-for-m-88.html",
    "trump-warns-the-shootin-starts-bigger-better-stronger-attack-on-iran-i-174.html",
    "trump-warns-the-shootin-starts-bigger-better-stronger-attack-on-iran-i-175.html",
    "in-the-crosshairs-trump-sending-2500-marines-invasion-ships-to-middle-162.html",
    "trump-casts-doubt-on-iran-peace-deal-and-says-tehran-has-not-paid-a-bi-179.html",
    "conspiracy-charges-for-protesters-the-landmark-2026-trial-everyone-is.html",
    "in-first-remarks-irans-new-supreme-leader-vows-to-avenge-martyrs-keep-156.html",

    # ❌ SENSATIONAL CRIME / CLICKBAIT NEWS
    "hard-proof-eerie-similarity-between-missing-girl-genesis-reid-casey-an-160.html",
    "drug-loot-boobs-airline-worker-splashed-out-on-boob-job-rolex-luxury-g-169.html",
    "cruise-ship-horror-over-150-sick-as-norovirus-outbreak-hits-star-princ-164.html",
    "travel-chaos-dubai-airport-flights-suspended-after-terrifying-iranian-168.html",
    "climbers-slip-terrifying-moment-mountaineer-slips-and-uncontrollably-h-161.html",

    # ❌ MISLEADING FINANCE / WEALTH CLICKBAIT
    "the-100-million-mortgage-secret-why-musk-and-zuckerberg-choose-debt-ov-159.html",
    "check-your-pockets-the-2000-sacagawea-dollar-rare-errors-worth-massive-42.html",
    "washington-quarters-worth-150k-rare-coins-that-look-ordinary-144.html",

    # ❌ DUAL USE / CONTROVERSIAL TECH
    "dual-use-tech-how-companies-sell-the-same-tools-for-aid-and-war-181.html",
    "ciscos-deep-ties-to-israeli-military-exposed-in-leaked-documents-185.html",
    "a-court-just-ruled-meta-and-youtube-negligent-social-media-may-never-b-171.html",

    # ❌ MISLEADING MISC CLICKBAIT
    "spaced-outasteroid-the-size-of-a-bus-speeding-near-earth-as-nasa-track-163.html",
    "eclipse-of-the-century-2026-6-minutes-of-total-darkness-mapped-best-vi-60.html",
    "count-the-cost-costco-shoppers-beware-retail-giant-pulls-popular-meal-167.html",
    "meaty-mania-four-big-changes-hitting-all-outback-steakhouse-locations-166.html",
    "texas-roadhouse-backtracks-on-100-id-alcohol-policy-after-pushback-ove-158.html",
]

# ============================================================
#  MAIN SCRIPT
# ============================================================

def delete_spam_articles():
    deleted = []
    not_found = []

    print("\n" + "="*60)
    print("  SPAM ARTICLES CLEANUP — techvibedetails.online")
    print("="*60)

    if not os.path.exists(ARTICLES_FOLDER):
        print(f"\n❌ ERROR: '{ARTICLES_FOLDER}' folder nahi mila!")
        print("   Script usi folder mein run karo jahan articles/ folder ho.")
        return [], []

    for filename in SPAM_FILES:
        filepath = os.path.join(ARTICLES_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            deleted.append(filename)
            print(f"  ✅ Deleted: {filename}")
        else:
            not_found.append(filename)
            print(f"  ⚠️  Not found: {filename}")

    return deleted, not_found


def update_sitemap(deleted_files):
    if not os.path.exists(SITEMAP_FILE):
        print(f"\n⚠️  sitemap.xml nahi mila — skip kar raha hun.")
        return

    print(f"\n{'='*60}")
    print("  SITEMAP UPDATE")
    print("="*60)

    # Deleted files ke URLs banao
    deleted_urls = set()
    for f in deleted_files:
        url = f"{SITE_URL}/articles/{f}"
        deleted_urls.add(url)

    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()

        # Namespace handle karo
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        urls_removed = 0
        for url_elem in root.findall(f"{ns}url"):
            loc = url_elem.find(f"{ns}loc")
            if loc is not None and loc.text in deleted_urls:
                root.remove(url_elem)
                urls_removed += 1
                print(f"  🗑️  Sitemap se remove: {loc.text}")

        # Updated sitemap save karo
        tree.write(SITEMAP_FILE, xml_declaration=True,
                   encoding="utf-8", default_namespace="")

        print(f"\n  ✅ Sitemap updated — {urls_removed} URLs remove ki gayin")

    except Exception as e:
        print(f"\n❌ Sitemap error: {e}")
        print("   Manually check karo sitemap.xml")


def print_summary(deleted, not_found):
    print(f"\n{'='*60}")
    print("  FINAL SUMMARY")
    print("="*60)
    print(f"  ✅ Total deleted  : {len(deleted)} articles")
    print(f"  ⚠️  Not found     : {len(not_found)} articles")
    print(f"  📅 Time           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if not_found:
        print(f"\n  ⚠️  Ye files nahi milin (already deleted ya naam alag hai):")
        for f in not_found:
            print(f"     - {f}")

    print(f"\n{'='*60}")
    print("  NEXT STEPS:")
    print("="*60)
    print("  1. git add .")
    print("  2. git commit -m 'Remove spam articles and update sitemap'")
    print("  3. git push")
    print("  4. Google Search Console > Sitemaps > Resubmit sitemap.xml")
    print("  5. Search Console > URL Inspection > Good articles manually request karo")
    print("="*60 + "\n")


# ============================================================
#  RUN
# ============================================================
if __name__ == "__main__":
    deleted, not_found = delete_spam_articles()
    update_sitemap(deleted)
    print_summary(deleted, not_found)