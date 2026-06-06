#!/usr/bin/env python3
"""Interactive demo launcher — pick a tool from the menu."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mlx.console import C, _c, banner, section, table

# (id, name, description, script, category)
DEMOS = [
    ("01", "List Profiles", "Workspaces, folders, profile search", "01_list_profiles.py", "core"),
    ("02", "Start / Stop", "Open profile, screenshot, auto-stop", "02_start_stop_profile.py", "core"),
    ("03", "Bulk Farm", "Run task across multiple profiles", "03_bulk_farm.py", "core"),
    ("04", "Cookie Backup", "Export cookies to JSON", "04_cookie_backup.py", "core"),
    ("05", "Proxy Check", "Validate single proxy", "05_proxy_check.py", "core"),
    ("06", "GitHub Login", "Automated GitHub sign-in", "06_github_login.py", "core"),
    ("07", "Social Warmup", "Visit sites to build trust", "07_social_warmup.py", "warmup"),
    ("08", "Quick Profile", "Disposable browser (v3 API)", "08_quick_profile.py", "core"),
    ("09", "Fingerprint Scan", "Bot detection test + report", "09_fingerprint_scan.py", "core"),
    ("10", "Google Login", "Google account sign-in flow", "10_google_login.py", "core"),
    ("11", "Facebook Warmup", "Scroll feed, simulate activity", "11_facebook_warmup.py", "social"),
    ("12", "Twitter Warmup", "Browse timeline, natural scroll", "12_twitter_warmup.py", "social"),
    ("13", "Bulk Clone", "Clone profiles via Cloud API", "13_bulk_clone_profiles.py", "core"),
    ("14", "Bulk Proxy Check", "Validate proxies from file", "14_bulk_proxy_check.py", "core"),
    ("15", "Cookie Restore", "Import cookies from JSON backup", "15_cookie_restore.py", "core"),
    ("16", "Profile Dashboard", "Full account overview", "16_profile_dashboard.py", "core"),
    ("17", "E-commerce Warmup", "Amazon/eBay browsing pattern", "17_ecommerce_warmup.py", "shop"),
    ("18", "Active Monitor", "Live running-profiles monitor", "18_active_monitor.py", "core"),
    ("19", "Mass Profile Creator", "Create 1000+ profiles from CSV", "19_mass_profile_creator.py", "core"),
    ("20", "Proxy Rotator", "Check live + assign to profiles", "20_proxy_rotator_assigner.py", "core"),
    ("21", "Cookie Bulk I/O", "Netscape/JSON import/export bulk", "21_cookie_injector_exporter.py", "core"),
    ("22", "Fingerprint Randomizer", "Refresh UA, Canvas, WebGL flags", "22_fingerprint_randomizer.py", "core"),
    ("23", "Local API Manager", "Launcher ports, active, stop-all", "23_local_api_manager.py", "core"),
    ("24", "News History", "CNN, BBC, Forbes browsing", "24_news_history_warmup.py", "warmup"),
    ("25", "Mouse Scroller", "Random mouse, scroll, click", "25_random_mouse_scroller.py", "warmup"),
    ("26", "Google Search Farmer", "Search keywords, click results", "26_google_search_farmer.py", "warmup"),
    ("27", "YouTube Watcher", "Search, watch, like videos", "27_youtube_watcher.py", "warmup"),
    ("28", "FB Initializer", "Cookie login + 5min feed warmup", "28_fb_account_initializer.py", "social"),
    ("29", "FB BM Accepter", "Accept Business Manager invite", "29_fb_bm_invitation_accepter.py", "social"),
    ("30", "TikTok Liker", "FYP scroll, like, follow", "30_tiktok_mass_liker.py", "social"),
    ("31", "Twitter Mention", "Cross-tag replies for trust", "31_twitter_mass_mention.py", "social"),
    ("32", "eBay Account Prep", "Clean env before registration", "32_ebay_account_prep.py", "shop"),
    ("33", "Amazon Wishlist", "Search product, add to list", "33_amazon_wishlist_adder.py", "shop"),
    ("34", "Etsy Traffic", "Organic shop visit pattern", "34_etsy_traffic_generator.py", "shop"),
    ("35", "MetaMask Setup", "Extension install + import flow", "35_metamask_installer.py", "crypto"),
    ("36", "Galxe Automator", "Quest board + OAuth login", "36_galxe_quest_automator.py", "crypto"),
    ("37", "Zealy Claimer", "Daily crew quest tasks", "37_zealy_quest_claimer.py", "crypto"),
    ("38", "Faucet Claimer", "Testnet + 2Captcha support", "38_faucet_claimer.py", "crypto"),
    ("39", "GMaps Review Quota", "Local SEO review scheduler", "39_gmaps_review_quota.py", "seo"),
    ("40", "Trustpilot Rating", "Referer warmup + 5-star", "40_trustpilot_rating.py", "seo"),
    ("41", "Yelp Stealth Review", "Residential proxy + mouse sim", "41_yelp_stealth_reviewer.py", "seo"),
    ("42", "Ticketmaster Queue", "Session warm + queue hold", "42_ticketmaster_queue_keeper.py", "checkout"),
    ("43", "Nike SNKRS Draw", "Login + captcha + draw entry", "43_nike_snkrs_draw.py", "checkout"),
    ("44", "Stripe VCC Checkout", "VCC fill + anti-decline", "44_stripe_vcc_checkout.py", "checkout"),
    ("45", "Turnstile Solver", "Cloudflare via CapSolver", "45_cloudflare_turnstile_solver.py", "crawler"),
    ("46", "DataDome Template", "Akamai/DataDome profile flags", "46_datadome_akamai_template.py", "crawler"),
    ("47", "reCAPTCHA v3 Farmer", "Invisible trust score build", "47_recaptcha_v3_farmer.py", "crawler"),
    ("48", "ADBLogin Migrator", "Convert + import to MLX", "48_adblogin_migrator.py", "migrate"),
    ("49", "AdsPower Exporter", "Export Dolphin/AdsPower cookies", "49_adspower_dolphin_exporter.py", "migrate"),
    ("50", "Incogniton Sync", "Backup restore to MLX", "50_incogniton_backup_sync.py", "migrate"),
    ("51", "YT Watch-Time Boost", "Multi-tab watch + ad skip", "51_youtube_watchtime_booster.py", "views"),
    ("52", "Twitch Viewer", "Live view + drop claim", "52_twitch_viewer_drops.py", "views"),
    ("53", "TikTok Live Bot", "Hearts + live comments", "53_tiktok_live_interaction.py", "views"),
]

CATEGORIES = {
    "core": "Profile & Proxy (Core)",
    "warmup": "Warm-up & Farming",
    "social": "Social Media & Ads",
    "shop": "E-Commerce & Dropship",
    "crypto": "Crypto & Airdrop",
    "seo": "Local SEO & Reviews",
    "checkout": "Sneaker & Ticket Checkout",
    "crawler": "Crawler & Anti-Bot",
    "migrate": "Migration & Sync",
    "views": "View & Watch-Time Farming",
}


def print_menu(filter_cat: str | None = None) -> None:
    rows = []
    for d in DEMOS:
        if filter_cat and d[4] != filter_cat:
            continue
        rows.append([d[0], d[1], CATEGORIES.get(d[4], d[4]), d[2]])
    table(["#", "Tool", "Category", "Description"], rows, max_col=32)


def main() -> None:
    banner("Multilogin X Demo Suite", "53 tools · Full packs + EXE → t.me/Multilogin_Scripts_Bot · SAAS50")
    print_menu()
    print()
    print(_c("  Commands: 01-53 | auto | cat seo|... | q quit", C.DIM))

    demos_dir = Path(__file__).resolve().parent
    while True:
        print()
        choice = input(_c("  demo> ", C.BOLD + C.MAGENTA)).strip().lower()
        if choice in ("q", "quit", "exit"):
            print(_c("  Bye.", C.DIM))
            break
        if choice in ("auto", "pipeline"):
            section("Auto Pipeline")
            subprocess.run([sys.executable, str(demos_dir / "auto_pipeline.py")], cwd=str(demos_dir.parent))
            continue
        if choice.startswith("cat "):
            cat = choice.split(maxsplit=1)[1]
            if cat in CATEGORIES:
                section(CATEGORIES[cat])
                print_menu(cat)
            else:
                print(_c("  Categories: core, warmup, social, shop, crypto, seo, checkout, crawler, migrate, views", C.YELLOW))
            continue
        if choice in ("all", "list", "?"):
            print_menu()
            continue
        match = next((d for d in DEMOS if d[0] == choice.zfill(2)), None)
        if not match:
            print(_c("  Unknown demo. Try 01-53 or cat seo", C.RED))
            continue
        script = demos_dir / match[3]
        if not script.exists():
            print(_c(f"  Missing script: {script.name}", C.RED))
            continue
        section(f"Running: {match[1]} [{CATEGORIES.get(match[4], '')}]")
        print(_c(f"  python {script.name}\n", C.DIM))
        try:
            subprocess.run([sys.executable, str(script)], cwd=str(demos_dir.parent))
        except KeyboardInterrupt:
            print(_c("\n  Interrupted.", C.YELLOW))


if __name__ == "__main__":
    main()
