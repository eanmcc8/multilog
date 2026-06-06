#!/usr/bin/env python3
"""Demo: reCAPTCHA v3 invisible trust score farmer."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.captcha import solve_recaptcha_v3
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import load_env, require_env
from mlx.human import human_delay, human_scroll, random_page_activity

load_env()

TRUST_SITES = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.reddit.com",
]


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    rounds = int(os.getenv("RECAPTCHA_FARM_ROUNDS", "5"))
    min_score = float(os.getenv("RECAPTCHA_MIN_SCORE", "0.7"))
    probe_url = os.getenv("RECAPTCHA_PROBE_URL", "")

    banner("reCAPTCHA v3 Trust Farmer", f"Score building  |  {timestamp()}")
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()

            for i in range(rounds):
                url = random.choice(TRUST_SITES)
                section(f"Round {i + 1}: {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=45000)
                await random_page_activity(page, scrolls=random.randint(2, 6), clicks=1)
                await human_delay(3000, 7000)
                ok("Human signals sent")

            if probe_url:
                section("Probe v3 token")
                await page.goto(probe_url, wait_until="domcontentloaded", timeout=60000)
                site_key_el = page.locator("[data-sitekey]")
                if await site_key_el.count():
                    site_key = await site_key_el.first.get_attribute("data-sitekey")
                    if site_key:
                        token = solve_recaptcha_v3(site_key, page.url, min_score=min_score)
                        if token:
                            ok(f"v3 token obtained (min_score={min_score})")
                        else:
                            warn("Set TWOCAPTCHA_API_KEY")
                await human_scroll(page, 400)

            ok("Trust farming session complete")


if __name__ == "__main__":
    asyncio.run(main())
