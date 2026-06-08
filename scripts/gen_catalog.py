#!/usr/bin/env python3
"""Generate demos/catalog.json from DEMOS list in demos/run.py.

Usage:
    python scripts/gen_catalog.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import DEMOS list directly from run.py
from demos.run import DEMOS  # noqa: E402

CATEGORY_LABELS = {
    "core":     "Profile & Proxy (Core)",
    "warmup":   "Warm-up & Browsing",
    "social":   "Social Media",
    "shop":     "E-Commerce & Travel",
    "crypto":   "Crypto & Web3",
    "seo":      "Local SEO & Listings",
    "checkout": "Checkout & Payments",
    "crawler":  "Crawler & Anti-Bot",
    "migrate":  "Migration & Sync",
    "media":    "Media & Streaming",
    "gaming":   "Gaming",
    "work":     "Freelance & Jobs",
    "ads":      "Ads Manager",
    "learn":    "E-Learning & Courses",
}

catalog = []
for num, name, description, script, category in DEMOS:
    catalog.append({
        "id": int(num),
        "number": num.zfill(3),
        "name": name,
        "description": description,
        "script": script,
        "category": category,
        "category_label": CATEGORY_LABELS.get(category, category.title()),
        "github_url": f"https://github.com/multilogin-automation/multilogin-automation/blob/main/demos/{script}",
    })

out = ROOT / "demos" / "catalog.json"
out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Written {len(catalog)} tools -> {out.relative_to(ROOT)}")
