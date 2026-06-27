"""Playwright async driver backend.

Usage (sync wrapper via asyncio.run is provided by StealthSession):

    profile = BrowserProfile.random(driver="playwright")
    async with PlaywrightDriver(profile) as drv:
        await drv.get("https://example.com")
        print(await drv.title())
"""
from __future__ import annotations

import asyncio
import json
import random
from pathlib import Path
from typing import Any


class PlaywrightDriver:
    """Async Playwright backend with full fingerprint injection."""

    def __init__(self, profile) -> None:
        self.profile = profile
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None

    async def __aenter__(self) -> "PlaywrightDriver":
        await self.start()
        return self

    async def __aexit__(self, *_) -> None:
        await self.stop()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self) -> "PlaywrightDriver":
        from playwright.async_api import async_playwright

        fp = self.profile.fingerprint
        self._pw = await async_playwright().__aenter__()

        launch_args = [
            "--no-first-run",
            "--no-service-autorun",
            "--password-store=basic",
            "--disable-blink-features=AutomationControlled",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
            f"--lang={fp.locale}",
        ] + self.profile.extra_args

        launch_kwargs: dict[str, Any] = {
            "headless": self.profile.headless,
            "args": launch_args,
        }
        if self.profile.proxy:
            launch_kwargs["proxy"] = self.profile.proxy.as_playwright_dict()

        self._browser = await self._pw.chromium.launch(**launch_kwargs)

        context_kwargs: dict[str, Any] = {
            "user_agent": fp.user_agent,
            "locale": fp.locale,
            "timezone_id": fp.timezone,
            "viewport": {"width": fp.resolution_width, "height": fp.resolution_height},
            "device_scale_factor": fp.pixel_ratio,
            "color_scheme": "light",
            "extra_http_headers": {
                "Accept-Language": f"{fp.locale},{fp.locale.split('-')[0]};q=0.9,en;q=0.8",
                "DNT": "1" if fp.do_not_track else "0",
            },
        }
        if self.profile.proxy:
            context_kwargs["proxy"] = self.profile.proxy.as_playwright_dict()
        if self.profile.data_dir:
            pass  # persistent context handled below

        if self.profile.data_dir:
            self._context = await self._pw.chromium.launch_persistent_context(
                self.profile.data_dir,
                **{**launch_kwargs, **context_kwargs},
            )
        else:
            self._context = await self._browser.new_context(**context_kwargs)

        await self._inject_fingerprint_scripts()
        self._page = await self._context.new_page()
        await self._inject_page_scripts(self._page)
        return self

    async def stop(self) -> None:
        try:
            if self._browser:
                await self._browser.close()
        finally:
            if self._pw:
                await self._pw.__aexit__(None, None, None)

    # ------------------------------------------------------------------
    # Fingerprint injection
    # ------------------------------------------------------------------

    async def _inject_fingerprint_scripts(self) -> None:
        fp = self.profile.fingerprint
        script = f"""
        Object.defineProperty(navigator, 'platform', {{get: () => '{fp.platform}'}});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {fp.hardware_concurrency}}});
        Object.defineProperty(navigator, 'deviceMemory', {{get: () => {fp.device_memory}}});
        Object.defineProperty(navigator, 'doNotTrack', {{get: () => {'1' if fp.do_not_track else 'null'}}});
        Object.defineProperty(screen, 'width', {{get: () => {fp.resolution_width}}});
        Object.defineProperty(screen, 'height', {{get: () => {fp.resolution_height}}});
        Object.defineProperty(screen, 'availWidth', {{get: () => {fp.resolution_width}}});
        Object.defineProperty(screen, 'availHeight', {{get: () => {fp.resolution_height - 40}}});
        Object.defineProperty(screen, 'colorDepth', {{get: () => {fp.color_depth}}});
        Object.defineProperty(screen, 'pixelDepth', {{get: () => {fp.color_depth}}});
        """
        if fp.webgl_vendor:
            script += f"""
        const origGetParam = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {{
            if (param === 37445) return '{fp.webgl_vendor}';
            if (param === 37446) return '{fp.webgl_renderer}';
            return origGetParam.call(this, param);
        }};
        const origGetParam2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(param) {{
            if (param === 37445) return '{fp.webgl_vendor}';
            if (param === 37446) return '{fp.webgl_renderer}';
            return origGetParam2.call(this, param);
        }};
            """
        if fp.canvas_noise > 0:
            script += f"""
        const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {{
            const ctx = this.getContext('2d');
            if (ctx) {{
                const img = ctx.getImageData(0, 0, this.width, this.height);
                for (let i = 0; i < img.data.length; i += 4) {{
                    img.data[i]   = Math.min(255, img.data[i]   + Math.floor(Math.random() * {fp.canvas_noise} * 10));
                    img.data[i+1] = Math.min(255, img.data[i+1] + Math.floor(Math.random() * {fp.canvas_noise} * 10));
                    img.data[i+2] = Math.min(255, img.data[i+2] + Math.floor(Math.random() * {fp.canvas_noise} * 10));
                }}
                ctx.putImageData(img, 0, 0);
            }}
            return origToDataURL.call(this, type);
        }};
            """
        if fp.audio_noise > 0:
            script += f"""
        const origGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function(channel) {{
            const data = origGetChannelData.call(this, channel);
            for (let i = 0; i < data.length; i++) {{
                data[i] += (Math.random() * 2 - 1) * {fp.audio_noise};
            }}
            return data;
        }};
            """
        await self._context.add_init_script(script)

    async def _inject_page_scripts(self, page) -> None:
        await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = {runtime: {}, loadTimes: function(){}, csi: function(){}, app: {}};
        Object.defineProperty(navigator, 'plugins', {get: () => [
            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: ''},
            {name: 'Native Client', filename: 'internal-nacl-plugin', description: ''},
        ]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    async def get(self, url: str, *, wait_until: str = "domcontentloaded", timeout: int = 30000) -> None:
        await self._page.goto(url, wait_until=wait_until, timeout=timeout)

    async def current_url(self) -> str:
        return self._page.url

    async def title(self) -> str:
        return await self._page.title()

    async def source(self) -> str:
        return await self._page.content()

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    async def find(self, selector: str):
        return self._page.locator(selector)

    async def click(self, selector: str) -> None:
        await self._page.click(selector)

    async def type(self, selector: str, text: str, *, delay: int | None = None) -> None:
        if delay is None:
            delay = random.randint(40, 120)
        await self._page.type(selector, text, delay=delay)

    async def screenshot(self, path: str) -> None:
        await self._page.screenshot(path=path, full_page=True)

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------

    async def get_cookies(self) -> list[dict]:
        return await self._context.cookies()

    async def set_cookies(self, cookies: list[dict]) -> None:
        await self._context.add_cookies(cookies)

    async def clear_cookies(self) -> None:
        await self._context.clear_cookies()

    # ------------------------------------------------------------------
    # JavaScript
    # ------------------------------------------------------------------

    async def execute_js(self, script: str, *args) -> Any:
        return await self._page.evaluate(script, *args)

    # ------------------------------------------------------------------
    # Extra helpers
    # ------------------------------------------------------------------

    @property
    def page(self):
        return self._page

    @property
    def context(self):
        return self._context

    async def new_page(self):
        page = await self._context.new_page()
        await self._inject_page_scripts(page)
        return page

    async def wait_for_selector(self, selector: str, timeout: int = 10000):
        return await self._page.wait_for_selector(selector, timeout=timeout)

    async def wait_for_load(self, state: str = "domcontentloaded", timeout: int = 30000) -> None:
        await self._page.wait_for_load_state(state, timeout=timeout)
