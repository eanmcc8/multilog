"""Demo 07 — Playwright warmup: open a page with a randomized profile.

Requires Playwright browsers installed:
    playwright install chromium

Run:
    python3 stealthbrowser/demos/demo_07_playwright_warmup.py
"""
from __future__ import annotations

import asyncio

from stealthbrowser.profile import BrowserProfile
from stealthbrowser.session import StealthSession
from stealthbrowser.human import (
    human_delay,
    human_scroll,
    random_mouse_wander,
    slow_read,
)


async def warmup(url: str = "https://www.wikipedia.org") -> None:
    profile = BrowserProfile.random(
        driver="playwright",
        os="windows",
        headless=True,
    )
    print(f"Profile : {profile.name}")
    print(f"UA      : {profile.fingerprint.user_agent[:70]}...")
    print(f"TZ      : {profile.fingerprint.timezone}")
    print(f"Locale  : {profile.fingerprint.locale}")
    print()

    async with StealthSession(profile) as s:
        print(f"Navigating to {url}...")
        await s.get(url)
        print(f"Title   : {await s.title()}")
        print(f"URL     : {await s.current_url()}")

        print("Simulating human activity...")
        await human_delay(800, 1500)
        await random_mouse_wander(s.page, moves=5)
        await human_scroll(s.page, 400)
        await slow_read(s.page, seconds=2)

        print("Taking screenshot -> output/warmup_demo.png")
        import pathlib
        pathlib.Path("output").mkdir(exist_ok=True)
        await s.screenshot("output/warmup_demo.png")

    print("Done.")


if __name__ == "__main__":
    asyncio.run(warmup())
