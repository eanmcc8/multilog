#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: news-site browsing to build clean browser history."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, fail, ok, section, timestamp
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, human_scroll, random_mouse_wander

NEWS_SITES = [
    ("CNN", "https://www.cnn.com"),
    ("BBC", "https://www.bbc.com/news"),
    ("Forbes", "https://www.forbes.com"),
    ("Reuters", "https://www.reuters.com"),
    ("NYTimes", "https://www.nytimes.com"),
]

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    count = int(os.getenv("NEWS_SITES_COUNT", "3"))
    sites = random.sample(NEWS_SITES, min(count, len(NEWS_SITES)))

    banner("News History Warmup", f"Clean browsing history  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            for name, url in sites:
                section(name)
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    await human_delay(2000, 5000)
                    await random_mouse_wander(page, random.randint(5, 12))
                    for _ in range(random.randint(4, 8)):
                        await human_scroll(page, random.randint(250, 600))
                        await human_delay(1500, 3500)
                    path = ensure_output() / f"news_{name.lower()}.png"
                    await page.screenshot(path=str(path))
                    ok(f"{name} visited -> {path.name}")
                except Exception as exc:
                    fail(str(exc))


if __name__ == "__main__":
    asyncio.run(main())
