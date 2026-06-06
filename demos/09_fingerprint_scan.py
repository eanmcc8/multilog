#!/usr/bin/env python3
"""Demo: fingerprint / bot-detection scan with screenshot report."""
import asyncio

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp
from mlx.env import ensure_output, load_env, require_env

SCAN_URLS = [
    ("Sannysoft", "https://bot.sannysoft.com/"),
    ("BrowserLeaks Canvas", "https://browserleaks.com/canvas"),
    ("PixelScan", "https://pixelscan.net/"),
]

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    banner("Fingerprint Scanner", f"Antidetect profile test  |  {timestamp()}")
    out = ensure_output() / "fingerprint_scan"
    out.mkdir(parents=True, exist_ok=True)

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            for name, url in SCAN_URLS:
                section(name)
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    await page.wait_for_timeout(3000)
                    safe = name.lower().replace(" ", "_")
                    path = out / f"{safe}.png"
                    await page.screenshot(path=str(path), full_page=True)
                    ok(f"Saved {path.name}")
                except Exception as exc:
                    fail(str(exc))

    section("Report")
    ok(f"All screenshots in {out}/")


if __name__ == "__main__":
    asyncio.run(main())
