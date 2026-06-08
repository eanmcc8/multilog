#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: Ticketmaster queue session keeper — warm profile and hold queue."""
import asyncio
import os

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ensure_output, load_env, require_env
from mlx.human import human_delay, random_mouse_wander

load_env()


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    event_url = os.getenv("TICKETMASTER_URL", "https://www.ticketmaster.com")
    hold_min = int(os.getenv("TM_QUEUE_HOLD_MIN", "15"))

    banner("Ticketmaster Queue Keeper", f"Session warm + hold  |  {timestamp()}")
    warn("Requires deep hardware fingerprint — see README Important Note")

    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Warm Ticketmaster session")
            await page.goto(event_url, wait_until="domcontentloaded", timeout=90000)
            await human_delay(5000, 10000)
            await random_mouse_wander(page, 6)

            section(f"Holding session ~{hold_min} min")
            elapsed = 0
            while elapsed < hold_min * 60:
                await page.wait_for_timeout(30_000)
                await random_mouse_wander(page, 2)
                elapsed += 30
                if "queue" in page.url.lower() or await page.locator("text=queue").count():
                    ok(f"In queue — holding ({elapsed}s)")
                else:
                    ok(f"Session alive ({elapsed}s)")

            path = ensure_output() / "ticketmaster_queue.png"
            await page.screenshot(path=str(path))
            ok(f"Screenshot -> {path.name}")


if __name__ == "__main__":
    asyncio.run(main())
