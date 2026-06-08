"""Playwright CDP helpers for Multilogin X profiles.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from mlx.client import MultiloginX
from mlx.models import ProfileSession


class PlaywrightSession:
    def __init__(self, mlx: MultiloginX, session: ProfileSession, browser, context):
        self.mlx = mlx
        self.session = session
        self.browser = browser
        self.context = context

    async def new_page(self):
        if self.context.pages:
            return self.context.pages[0]
        return await self.context.new_page()

    async def close(self) -> None:
        try:
            await self.browser.close()
        finally:
            self.mlx.stop_profile(self.session.profile_id, self.session.folder_id or None)


async def connect_playwright(mlx: MultiloginX, session: ProfileSession, playwright):
    browser = await playwright.chromium.connect_over_cdp(session.browser_url, timeout=15000)
    context = browser.contexts[0] if browser.contexts else await browser.new_context()
    return browser, context


@asynccontextmanager
async def profile_browser(
    mlx: MultiloginX,
    profile_id: str,
    folder_id: str,
    playwright,
    *,
    headless: bool = False,
) -> AsyncIterator[PlaywrightSession]:
    session = mlx.start_profile(profile_id, folder_id, headless=headless)
    browser, context = await connect_playwright(mlx, session, playwright)
    ps = PlaywrightSession(mlx, session, browser, context)
    try:
        yield ps
    finally:
        await ps.close()
