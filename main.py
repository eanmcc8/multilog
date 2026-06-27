"""
StealthBrowser — standalone multi-backend browser automation module.

Backends  : Playwright · Selenium/undetected-chromedriver · HTTP (httpx/requests)
No external service required.  Profiles are local and fully customizable.

Quick start:
  python3 stealthbrowser/demos/demo_01_http_fetch.py
  python3 stealthbrowser/demos/demo_02_profile_batch.py
  python3 stealthbrowser/demos/demo_03_farm_http.py
  python3 stealthbrowser/demos/demo_04_fingerprint_report.py

CLI:
  stealthbrowser profile create --os windows --driver http
  stealthbrowser profile batch  --count 10 --prefix MyProfile -o profiles.json
  stealthbrowser fingerprint    --os macos
  stealthbrowser fetch          https://httpbin.org/headers --title
"""

import sys
import json

from stealthbrowser import __version__
from stealthbrowser.profile import BrowserProfile, Fingerprint


def main() -> None:
    print(f"StealthBrowser v{__version__}")
    print("Standalone multi-backend browser automation — no external service required.")
    print()

    # Show a quick fingerprint sample for each OS
    print("Sample fingerprints:")
    for os_name in ("windows", "macos", "linux"):
        fp = Fingerprint.random(os_name)
        print(f"  [{os_name:7s}] {fp.user_agent[:65]}...")
        print(f"           {fp.resolution_width}x{fp.resolution_height}  "
              f"{fp.locale}  {fp.timezone}  cores={fp.hardware_concurrency}")
    print()

    print("Run a demo:")
    demos = [
        ("demo_01", "HTTP fetch with random fingerprint"),
        ("demo_02", "Batch-create & save profiles"),
        ("demo_03", "HTTP farm across 4 profiles"),
        ("demo_04", "Fingerprint report (all OS types)"),
        ("demo_05", "Proxy pool rotation"),
        ("demo_06", "Cookie utilities"),
        ("demo_07", "Playwright warmup (needs: playwright install chromium)"),
    ]
    for name, desc in demos:
        print(f"  python3 stealthbrowser/demos/{name}_*.py  — {desc}")
    print()
    print("CLI:  stealthbrowser --help")


if __name__ == "__main__":
    main()
    sys.exit(0)
