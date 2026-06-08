#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share = free tool drops
"""Demo: Reddit community warmup — browse subreddits with human scroll."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll

load_env()

SUBS = ["python", "technology", "worldnews", "gaming"]


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    subs = random.sample(SUBS, min(int(os.getenv("REDDIT_SUBS", "3")), len(SUBS)))
    dry = os.getenv("REDDIT_DRY_RUN", "true").lower() != "false"
    banner("Reddit Community Warmup", f"Subs: {', '.join(subs)}  |  {timestamp()}")
    warn("Vote manipulation violates Reddit rules — upvote disabled unless REDDIT_DRY_RUN=false")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            for sub in subs:
                await page.goto(f"https://www.reddit.com/r/{sub}/", wait_until="domcontentloaded", timeout=60000)
                await human_delay(3000, 6000)
                await human_scroll(page, random.randint(400, 900))
                up = page.locator('button[aria-label="upvote"], button[aria-label="Upvote"]')
                if await up.count() and not dry:
                    await up.first.click()
                    ok(f"Upvoted on r/{sub}")
                else:
                    warn(f"r/{sub} browsed (dry-run={dry})")
                await human_delay(2000, 4000)


if __name__ == "__main__":
    asyncio.run(main())
