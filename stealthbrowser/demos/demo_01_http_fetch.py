"""Demo 01 — HTTP driver: fetch a page with a random fingerprint."""
from __future__ import annotations

from stealthbrowser.profile import BrowserProfile
from stealthbrowser.session import StealthSession

profile = BrowserProfile.random(driver="http", os="windows")
print(f"Profile : {profile.name}")
print(f"UA      : {profile.fingerprint.user_agent[:60]}...")
print(f"Locale  : {profile.fingerprint.locale}")
print(f"TZ      : {profile.fingerprint.timezone}")
print()

with StealthSession(profile) as s:
    s.get("https://httpbin.org/headers")
    print("Status :", s.status_code())
    print("Title  :", s.title())
    print()
    print("Response (first 600 chars):")
    print(s.source()[:600])
