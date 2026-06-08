#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Google search farmer — type keywords and click random results."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp, warn
from mlx.env import ROOT, load_env, require_env
from mlx.human import human_delay, human_scroll, human_type

KEYWORDS_FILE = ROOT / "keywords.txt"
DEFAULT_KEYWORDS = ["best coffee beans", "python automation", "travel europe 2026", "healthy recipes"]

load_env()


def load_keywords() -> list[str]:
    if KEYWORDS_FILE.exists():
        lines = [
            l.strip()
            for l in KEYWORDS_FILE.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")
        ]
        if lines:
            return lines
    KEYWORDS_FILE.write_text("\n".join(DEFAULT_KEYWORDS) + "\n", encoding="utf-8")
    return DEFAULT_KEYWORDS


async def search_once(page, keyword: str) -> None:
    await page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=45000)
    await human_delay(1000, 2500)
    consent = page.locator('button:has-text("Accept"), button:has-text("Agree")')
    if await consent.count():
        await consent.first.click()
        await human_delay(500, 1200)

    box = 'textarea[name="q"], input[name="q"]'
    await human_type(page, box, keyword)
    await page.keyboard.press("Enter")
    await human_delay(2000, 4000)

    links = page.locator("#search a h3")
    count = await links.count()
    if count == 0:
        warn(f"No results for: {keyword}")
        return
    idx = random.randint(0, min(count - 1, 4))
    await links.nth(idx).click()
    await human_delay(3000, 6000)
    await human_scroll(page, random.randint(300, 700))
    ok(f"Clicked result #{idx + 1} for '{keyword}'")


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    queries = int(os.getenv("GOOGLE_SEARCH_COUNT", "3"))
    keywords = random.sample(load_keywords(), min(queries, len(load_keywords())))

    banner("Google Search Farmer", f"Search + click results  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            for kw in keywords:
                section(kw)
                try:
                    await search_once(page, kw)
                except Exception as exc:
                    fail(str(exc))


if __name__ == "__main__":
    asyncio.run(main())
