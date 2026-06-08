#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Galxe quest automator — login via Twitter/Discord and browse quests."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    campaign = os.getenv("GALXE_CAMPAIGN_URL", "https://galxe.com")

    banner("Galxe Task Automator", f"OAT / quest flow  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Open Galxe")
            await page.goto(campaign, wait_until="domcontentloaded", timeout=60000)
            await human_delay(3000, 6000)

            connect = page.locator('button:has-text("Log in"), button:has-text("Connect")')
            if await connect.count():
                ok("Galxe loaded — connect Twitter/Discord in browser")
                warn("Pre-login Twitter/X in same profile for smoother OAuth")

            section("Browse quests")
            await human_scroll(page, 600)
            await human_delay(4000, 8000)

            claim = page.locator('button:has-text("Claim"), button:has-text("Verify")')
            if await claim.count():
                if os.getenv("GALXE_AUTO_CLAIM", "false").lower() == "true":
                    await claim.first.click()
                    ok("Claim clicked")
                else:
                    warn("Set GALXE_AUTO_CLAIM=true to auto-click Claim")
            ok("Galxe session ready — extend with campaign-specific selectors")


if __name__ == "__main__":
    asyncio.run(main())
