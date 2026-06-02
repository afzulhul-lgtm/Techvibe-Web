import json
import os
import shutil
from datetime import datetime

# ============================================================
#   data.json CLEANUP SCRIPT — techvibedetails.online
#   Run: python clean_data_json.py
# ============================================================

DATA_FILE = "articles/data.json"

# Ye wahi filenames hain jo pehle articles/ se delete ki thin
SPAM_FILENAMES = [
    # FAKE PAYMENT / FINANCE
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
    "massive-4983-direct-deposit-2026-for-us-citizens-full-eligibility-exac-64.html",
    "irs-2000-direct-deposit-fully-explained-for-february-2026-dont-miss-ou-70.html",

    # FAKE WEATHER / EMERGENCY
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

    # FAKE DRIVING LAW (DUPLICATE)
    "critical-alert-the-new-2026-driving-law-affecting-all-50-states-ignore-66.html",
    "urgent-warning-strict-new-february-2026-driving-law-could-mean-fines-j-65.html",
    "urgent-alert-for-us-drivers-the-new-february-2026-driving-law-that-cou-33.html",

    # FAKE / MISLEADING TECH
    "gpt-56-leak-release-date-features-what-openai-isnt-telling-us.html",
    "your-bosss-tracking-software-is-secretly-sharing-your-data-with-google.html",
    "google-ai-search-backlash-users-threaten-mass-exodus-over-misinformati.html",
    "warning-hackers-are-sending-fake-jpeg-photos-that-silently-take-over-y-184.html",
    "tiny-startup-humiliates-nvidia-and-amd-runs-700b-ai-models-on-a-0-clou-183.html",
    "m5-macbook-pro-hinge-causes-sparks-and-catches-fire-just-two-days-afte-178.html",

    # SENSATIONAL SCIENCE
    "scientists-shock-the-world-have-we-completely-miscalculated-the-earths-26.html",
    "everything-we-knew-is-wrong-dinosaurs-and-mammoths-were-shockingly-slo-34.html",
    "quantum-physics-shocker-electrons-dont-entangle-all-at-once-the-mind-b-90.html",
    "mind-blowing-science-why-sweet-potatoes-and-regular-potatoes-are-actua-84.html",
    "long-before-trees-earth-was-ruled-by-this-mysterious-giant-lifeform-9.html",

    # FAKE MEDICAL CLICKBAIT
    "medical-miracle-groundbreaking-strategy-finally-forces-cancer-cells-to-89.html",
    "medical-breakthrough-doctors-finally-reveal-why-you-get-leisure-migrai-83.html",
    "over-65-and-losing-flexibility-new-study-reveals-its-not-your-muscles-87.html",
    "psychologists-warn-these-9-common-parenting-mistakes-are-guaranteed-to-91.html",
    "critical-alert-vets-issue-urgent-life-saving-warning-to-all-cat-owners-85.html",

    # FAKE MILITARY / POLITICAL
    "global-alert-uss-gerald-r-ford-deployed-to-europe-as-us-prepares-for-m-88.html",
    "trump-warns-the-shootin-starts-bigger-better-stronger-attack-on-iran-i-174.html",
    "trump-warns-the-shootin-starts-bigger-better-stronger-attack-on-iran-i-175.html",
    "in-the-crosshairs-trump-sending-2500-marines-invasion-ships-to-middle-162.html",
    "trump-casts-doubt-on-iran-peace-deal-and-says-tehran-has-not-paid-a-bi-179.html",
    "conspiracy-charges-for-protesters-the-landmark-2026-trial-everyone-is.html",
    "in-first-remarks-irans-new-supreme-leader-vows-to-avenge-martyrs-keep-156.html",

    # SENSATIONAL CRIME / CLICKBAIT
    "hard-proof-eerie-similarity-between-missing-girl-genesis-reid-casey-an-160.html",
    "drug-loot-boobs-airline-worker-splashed-out-on-boob-job-rolex-luxury-g-169.html",
    "cruise-ship-horror-over-150-sick-as-norovirus-outbreak-hits-star-princ-164.html",
    "travel-chaos-dubai-airport-flights-suspended-after-terrifying-iranian-168.html",
    "climbers-slip-terrifying-moment-mountaineer-slips-and-uncontrollably-h-161.html",

    # MISLEADING FINANCE / WEALTH
    "the-100-million-mortgage-secret-why-musk-and-zuckerberg-choose-debt-ov-159.html",
    "check-your-pockets-the-2000-sacagawea-dollar-rare-errors-worth-massive-42.html",
    "washington-quarters-worth-150k-rare-coins-that-look-ordinary-144.html",

    # CONTROVERSIAL / DUAL USE
    "dual-use-tech-how-companies-sell-the-same-tools-for-aid-and-war-181.html",
    "ciscos-deep-ties-to-israeli-military-exposed-in-leaked-documents-185.html",
    "a-court-just-ruled-meta-and-youtube-negligent-social-media-may-never-b-171.html",

    # MISC CLICKBAIT
    "spaced-outasteroid-the-size-of-a-bus-speeding-near-earth-as-nasa-track-163.html",
    "eclipse-of-the-century-2026-6-minutes-of-total-darkness-mapped-best-vi-60.html",
    "count-the-cost-costco-shoppers-beware-retail-giant-pulls-popular-meal-167.html",
    "meaty-mania-four-big-changes-hitting-all-outback-steakhouse-locations-166.html",
    "texas-roadhouse-backtracks-on-100-id-alcohol-policy-after-pushback-ove-158.html",
]

# ============================================================
def clean_data_json():
    print("\n" + "="*60)
    print("  data.json CLEANUP — techvibedetails.online")
    print("="*60)

    if not os.path.exists(DATA_FILE):
        print(f"\n❌ ERROR: '{DATA_FILE}' nahi mila!")
        print("   Script usi folder mein run karo jahan data.json hai.")
        return

    # Backup bana lo pehle
    backup_name = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy(DATA_FILE, backup_name)
    print(f"\n  💾 Backup bana diya: {backup_name}")

    # data.json load karo
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    total_before = len(articles)
    spam_set = set(SPAM_FILENAMES)

    removed = []
    kept = []

    for article in articles:
        filename = article.get("filename", "")
        if filename in spam_set:
            removed.append(article)
            print(f"  🗑️  Removed: [{article['id']}] {article['title'][:60]}...")
        else:
            kept.append(article)

    # Clean data save karo
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(kept, f, indent=4, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("  FINAL SUMMARY")
    print("="*60)
    print(f"  📊 Pehle total articles : {total_before}")
    print(f"  🗑️  Removed (spam)       : {len(removed)}")
    print(f"  ✅ Baqi (clean)          : {len(kept)}")
    print(f"  💾 Backup file           : {backup_name}")
    print(f"  📅 Time                  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*60}")
    print("  NEXT STEPS:")
    print("="*60)
    print("  1. Website check karo locally — cards sahi hain?")
    print("  2. git add .")
    print("  3. git commit -m 'Remove spam entries from data.json'")
    print("  4. git push")
    print("="*60 + "\n")

if __name__ == "__main__":
    clean_data_json()