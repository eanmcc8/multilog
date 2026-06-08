#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: MetaMask extension setup flow via Playwright (import seed optional)."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import require_env
from mlx.human import human_delay

METAMASK_CRX_HINT = "Install MetaMask from Chrome Web Store in profile first"


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    seed = os.getenv("METAMASK_SEED", "")

    banner("MetaMask Auto Installer", f"Wallet extension flow  |  {timestamp()}")
    warn("Never commit real seed phrases — use .env only")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Chrome Web Store — MetaMask")
            await page.goto(
                "https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            await human_delay(3000, 5000)

            add_btn = page.locator('button:has-text("Add to Chrome"), button:has-text("Install")')
            if await add_btn.count():
                ok("MetaMask page loaded — click Install in browser if prompted")
            else:
                warn(METAMASK_CRX_HINT)

            if seed:
                section("Import wallet (env seed)")
                words = seed.split()
                if len(words) not in (12, 24):
                    warn("METAMASK_SEED should be 12 or 24 words")
                else:
                    warn("Complete import in extension popup — automation varies by MLX extension UI")
                    ok(f"Seed loaded ({len(words)} words) — handle in open profile")
            else:
                warn("Set METAMASK_SEED + METAMASK_PASSWORD in .env for import step")

            section("Open extension home")
            await page.goto("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html", timeout=15000)
            await human_delay(2000, 4000)
            ok("MetaMask flow ready — finish setup in profile UI")


if __name__ == "__main__":
    asyncio.run(main())
