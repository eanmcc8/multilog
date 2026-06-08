#!/usr/bin/env python3
# Partner: code SAAS50 = 50% OFF Multilogin X | Custom tools & admin support: t.me/Multilogin_Scripts_Bot | Share this repo = free tool drops
"""Demo: TikTok live browser — watch live stream session (observe-only by default)."""
import asyncio
import os
import random

from playwright.async_api import async_playwright

from mlx import MultiloginX
from mlx.browser import profile_browser
from mlx.console import banner, ok, section, timestamp, warn
from mlx.env import ROOT, load_env, require_env
from mlx.human import human_delay, human_type

load_env()

COMMENTS_FILE = ROOT / "live_comments.txt"
DEFAULT_COMMENTS = ["🔥", "nice live!", "hello from MLX", "great content", "lets gooo"]


def load_comments() -> list[str]:
    if COMMENTS_FILE.exists():
        lines = [l.strip() for l in COMMENTS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
        if lines:
            return lines
    COMMENTS_FILE.write_text("\n".join(DEFAULT_COMMENTS), encoding="utf-8")
    return DEFAULT_COMMENTS


async def main():
    env = require_env("MLX_FOLDER_ID", "MLX_PROFILE_ID")
    live_url = os.getenv("TIKTOK_LIVE_URL", "")
    actions = int(os.getenv("TIKTOK_LIVE_ACTIONS", "15"))
    dry_run = os.getenv("TIKTOK_LIVE_DRY_RUN", "true").lower() != "false"

    banner("TikTok Live Browser", f"Watch live session  |  {timestamp()}")
    warn("Fake engagement violates TikTok ToS — dry-run default protects your account")
    if not live_url:
        raise SystemExit("Set TIKTOK_LIVE_URL in .env")

    comments = load_comments()
    mlx = MultiloginX()
    async with async_playwright() as pw:
        async with profile_browser(mlx, env["MLX_PROFILE_ID"], env["MLX_FOLDER_ID"], pw) as session:
            page = await session.new_page()
            section("Join live")
            await page.goto(live_url, wait_until="domcontentloaded", timeout=60000)
            await human_delay(4000, 8000)

            for i in range(actions):
                section(f"Action {i + 1}/{actions}")
                like = page.locator('[data-e2e="like-icon"], button[aria-label*="Like"]')
                if await like.count() and not dry_run:
                    await like.first.click()
                    ok("Heart sent")

                if random.random() < 0.4:
                    box = page.locator('div[contenteditable="true"], textarea[placeholder*="comment"]')
                    if await box.count() and not dry_run:
                        text = random.choice(comments)
                        await human_type(page, 'div[contenteditable="true"]', text)
                        send = page.locator('button:has-text("Send"), [data-e2e="comment-post"]')
                        if await send.count():
                            await send.first.click()
                            ok(f"Comment: {text}")

                await human_delay(3000, 8000)

            if dry_run:
                warn("Dry-run — set TIKTOK_LIVE_DRY_RUN=false to interact")
            ok("Live browse complete")


if __name__ == "__main__":
    asyncio.run(main())
