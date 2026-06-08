#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Interactive demo launcher — pick a tool from the menu."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mlx.console import C, _c, banner, promo_footer, section, table

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
    ("26", "Google Search Warmup", "Search keywords, click results", "26_google_search_warmup.py", "warmup"),
    ("27", "YouTube Watcher", "Search, watch, like videos", "27_youtube_watcher.py", "warmup"),
    ("28", "FB Initializer", "Cookie login + 5min feed warmup", "28_fb_account_initializer.py", "social"),
    ("29", "FB BM Accepter", "Accept Business Manager invite", "29_fb_bm_invitation_accepter.py", "social"),
    ("30", "TikTok Feed Warmup", "FYP scroll and browse", "30_tiktok_feed_warmup.py", "social"),
    ("31", "Twitter Engagement", "Timeline browse + compose", "31_twitter_engagement_warmup.py", "social"),
    ("32", "eBay Account Prep", "Clean env before registration", "32_ebay_account_prep.py", "shop"),
    ("33", "Amazon Wishlist", "Search product, add to list", "33_amazon_wishlist_adder.py", "shop"),
    ("34", "Etsy Shop Warmup", "Organic shop browse", "34_etsy_shop_warmup.py", "shop"),
    ("35", "MetaMask Setup", "Extension install + import flow", "35_metamask_installer.py", "crypto"),
    ("36", "Galxe Automator", "Quest board + OAuth login", "36_galxe_quest_automator.py", "crypto"),
    ("37", "Zealy Claimer", "Daily crew quest tasks", "37_zealy_quest_claimer.py", "crypto"),
    ("38", "Testnet Faucet", "Dev testnet + 2Captcha", "38_testnet_faucet_browser.py", "crypto"),
    ("39", "GMaps Listing", "Business page browse (read-only)", "39_gmaps_listing_browser.py", "seo"),
    ("40", "Trustpilot Browser", "Business page research", "40_trustpilot_page_browser.py", "seo"),
    ("41", "Yelp Listing", "Business listing browse", "41_yelp_listing_browser.py", "seo"),
    ("42", "Ticketmaster Warmup", "Event browse + session", "42_ticketmaster_session_warmup.py", "checkout"),
    ("43", "Nike SNKRS Browser", "Launch page browse", "43_nike_snkrs_browser.py", "checkout"),
    ("44", "Stripe Checkout QA", "Payment flow tester", "44_stripe_checkout_tester.py", "checkout"),
    ("45", "Turnstile Solver", "Cloudflare via CapSolver", "45_cloudflare_turnstile_solver.py", "crawler"),
    ("46", "DataDome Template", "Akamai/DataDome profile flags", "46_datadome_akamai_template.py", "crawler"),
    ("47", "reCAPTCHA v3 Probe", "Own-site score test", "47_recaptcha_v3_score_probe.py", "crawler"),
    ("48", "ADBLogin Migrator", "Convert + import to MLX", "48_adblogin_migrator.py", "migrate"),
    ("49", "AdsPower Exporter", "Export Dolphin/AdsPower cookies", "49_adspower_dolphin_exporter.py", "migrate"),
    ("50", "Incogniton Sync", "Backup restore to MLX", "50_incogniton_backup_sync.py", "migrate"),
    ("51", "YouTube Session", "Natural watch warmup", "51_youtube_session_warmup.py", "media"),
    ("52", "Twitch Stream", "Live stream browser", "52_twitch_stream_browser.py", "media"),
    ("53", "TikTok Live", "Live stream browser", "53_tiktok_live_browser.py", "media"),
    ("54", "Instagram Warmup", "Feed scroll + explore", "54_instagram_warmup.py", "social"),
    ("55", "LinkedIn Warmup", "B2B feed activity", "55_linkedin_warmup.py", "social"),
    ("56", "Pinterest Warmup", "Pin discovery browse", "56_pinterest_warmup.py", "social"),
    ("57", "Reddit Warmup", "Subreddit browse", "57_reddit_community_warmup.py", "social"),
    ("58", "Discord Warmup", "Web client channels", "58_discord_warmup.py", "social"),
    ("59", "Shopify Warmup", "Store browse pattern", "59_shopify_store_warmup.py", "shop"),
    ("60", "Shopee Warmup", "SEA marketplace browse", "60_shopee_warmup.py", "shop"),
    ("61", "Walmart Warmup", "US retail browse", "61_walmart_warmup.py", "shop"),
    ("62", "WhatsApp Web", "WA Web session hold", "62_whatsapp_web_warmup.py", "social"),
    ("63", "Telegram Web", "TG Web chat scroll", "63_telegram_web_warmup.py", "social"),
    ("64", "Health Audit", "Profile pre-flight check", "64_profile_health_audit.py", "core"),
    ("65", "Bulk Renamer", "Prefix rename profiles", "65_bulk_profile_renamer.py", "core"),
    ("66", "Binance Warmup", "Exchange market browse", "66_binance_warmup.py", "crypto"),
    ("67", "OpenSea Browser", "NFT marketplace browse", "67_opensea_browser.py", "crypto"),
    ("68", "Captcha Balance", "2Captcha / CapSolver wallet", "68_captcha_balance_check.py", "crawler"),
    ("69", "Session Keepalive", "Long session pulse", "69_session_keepalive.py", "core"),
    ("70", "Threads Warmup", "Meta Threads feed", "70_threads_meta_warmup.py", "social"),
    ("71", "Snapchat Web", "Stories + discover", "71_snapchat_web_warmup.py", "social"),
    ("72", "AliExpress", "Product search browse", "72_aliexpress_warmup.py", "shop"),
    ("73", "Travel Warmup", "Booking + Airbnb", "73_booking_travel_warmup.py", "shop"),
    ("74", "PayPal Session", "Dashboard browse", "74_paypal_session_warmup.py", "checkout"),
    ("75", "Steam Store", "Game store browser", "75_steam_game_browser.py", "gaming"),
    ("76", "Spotify Listener", "Playlist session", "76_spotify_listener_warmup.py", "media"),
    ("77", "Upwork Browser", "Freelance job feed", "77_upwork_freelancer_browser.py", "work"),
    ("78", "Google Ads", "Ads Manager dashboard", "78_google_ads_manager_browser.py", "ads"),
    ("79", "Meta Ads", "Facebook Ads Manager", "79_facebook_ads_manager_browser.py", "ads"),
    ("80", "Indeed Jobs", "Job search browse", "80_indeed_job_search_warmup.py", "work"),
    ("81", "Temu / Shein", "Discount shop browse", "81_temu_shop_warmup.py", "shop"),
    ("82", "Coinbase", "Crypto market browse", "82_coinbase_warmup.py", "crypto"),
    ("83", "Quora Warmup", "Community feed browse", "83_quora_community_warmup.py", "social"),
    ("84", "Mercari / Poshmark", "Resale marketplace", "84_mercari_resale_warmup.py", "shop"),
    ("85", "Bing Search", "Keyword search warmup", "85_bing_search_warmup.py", "warmup"),
    ("86", "DuckDuckGo Search", "Privacy search warmup", "86_duckduckgo_search_warmup.py", "warmup"),
    ("87", "Craigslist", "Local classifieds browse", "87_craigslist_listings_browser.py", "shop"),
    ("88", "Zillow Real Estate", "Property listing browse", "88_zillow_realestate_browser.py", "shop"),
    ("89", "Netflix Session", "Catalog browse warmup", "89_netflix_session_warmup.py", "media"),
    ("90", "Medium / Substack", "Article reader warmup", "90_medium_substack_reader.py", "social"),
    ("91", "Slack Web", "Workspace channel browse", "91_slack_web_warmup.py", "work"),
    ("92", "Outlook Web", "Inbox session warmup", "92_microsoft_outlook_warmup.py", "work"),
    ("93", "DoorDash", "Restaurant menu browse", "93_doordash_delivery_warmup.py", "shop"),
    ("94", "Fiverr Gigs", "Freelance gig browse", "94_fiverr_freelancer_browser.py", "work"),
    ("95", "Kraken Exchange", "Crypto market browse", "95_kraken_crypto_warmup.py", "crypto"),
    ("96", "SoundCloud", "Track listener warmup", "96_soundcloud_listener_warmup.py", "media"),
    ("97", "Tumblr Feed", "Community dashboard", "97_tumblr_community_warmup.py", "social"),
    ("98", "Roblox Discover", "Game catalog browse", "98_roblox_game_browser.py", "gaming"),
    ("99", "Namecheap Domains", "Domain search browse", "99_namecheap_domain_browser.py", "core"),
    ("100", "Google Scholar", "Academic paper search", "100_google_scholar_research_browser.py", "warmup"),
    ("101", "Uber Eats", "Food delivery browse", "101_uber_eats_delivery_warmup.py", "shop"),
    ("102", "Canva", "Design template browse", "102_canva_design_browser.py", "work"),
    ("103", "Notion", "Workspace page browse", "103_notion_workspace_warmup.py", "work"),
    ("104", "Zoom Web", "Meeting portal session", "104_zoom_meeting_warmup.py", "work"),
    ("105", "MS Teams", "Teams chat browse", "105_microsoft_teams_warmup.py", "work"),
    ("106", "Mastodon", "Federated timeline", "106_mastodon_social_warmup.py", "social"),
    ("107", "Bluesky", "AT Protocol feed", "107_bluesky_feed_warmup.py", "social"),
    ("108", "Coursera", "Course catalog browse", "108_coursera_learning_browser.py", "learn"),
    ("109", "Udemy", "Course search browse", "109_udemy_course_browser.py", "learn"),
    ("110", "Patreon", "Creator page browse", "110_patreon_creator_browser.py", "social"),
    ("111", "Stack Overflow", "Dev Q&A research", "111_stackoverflow_research_browser.py", "work"),
    ("112", "Product Hunt", "Launch discover feed", "112_producthunt_discover_browser.py", "work"),
    ("113", "Glassdoor", "Company research browse", "113_glassdoor_company_browser.py", "work"),
    ("114", "Target", "US retail deals browse", "114_target_retail_warmup.py", "shop"),
    ("115", "Best Buy", "Electronics browse", "115_bestbuy_electronics_warmup.py", "shop"),
    ("116", "Wise", "International payments", "116_wise_transfer_warmup.py", "checkout"),
    ("117", "Revolut", "Banking web session", "117_revolut_banking_warmup.py", "checkout"),
    ("118", "Phantom Wallet", "Solana web3 browse", "118_phantom_wallet_browser.py", "crypto"),
    ("119", "Uniswap DEX", "DeFi swap interface", "119_uniswap_dex_browser.py", "crypto"),
    ("120", "Hacker News", "Tech news front page", "120_hacker_news_reader.py", "warmup"),
]

CATEGORIES = {
    "core": "Profile & Proxy (Core)",
    "warmup": "Warm-up & Browsing",
    "social": "Social Media",
    "shop": "E-Commerce & Travel",
    "crypto": "Crypto & Web3",
    "seo": "Local SEO & Listings",
    "checkout": "Checkout & Payments",
    "crawler": "Crawler & Anti-Bot",
    "migrate": "Migration & Sync",
    "media": "Media & Streaming",
    "gaming": "Gaming",
    "work": "Freelance & Jobs",
    "ads": "Ads Manager",
    "learn": "E-Learning & Courses",
}


def print_menu(filter_cat: str | None = None) -> None:
    rows = []
    for d in DEMOS:
        if filter_cat and d[4] != filter_cat:
            continue
        rows.append([d[0], d[1], CATEGORIES.get(d[4], d[4]), d[2]])
    table(["#", "Tool", "Category", "Description"], rows, max_col=32)


def main() -> None:
    banner("Multilogin X Demo Suite", "120 tools · code SAAS50 = 50% OFF · @Multilogin_Scripts_Bot")
    promo_footer()
    print_menu()
    print()
    print(_c("  Commands: 01-120 | auto | cat seo|... | q quit", C.DIM))

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
                print(_c("  Categories: core, warmup, social, shop, crypto, seo, checkout, crawler, migrate, media, gaming, work, ads, learn", C.YELLOW))
            continue
        if choice in ("all", "list", "?"):
            print_menu()
            continue
        match = next((d for d in DEMOS if d[0] == (choice if len(choice) > 2 else choice.zfill(2))), None)
        if not match:
            print(_c("  Unknown demo. Try 01-120 or cat social", C.RED))
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
