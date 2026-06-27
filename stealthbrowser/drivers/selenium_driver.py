"""Selenium / undetected-chromedriver backend.

Falls back gracefully to regular selenium if undetected_chromedriver is not
installed.  All fingerprint properties are injected via CDP and JS on start.
"""
from __future__ import annotations

import json
import random
import time
from typing import Any

from stealthbrowser.drivers.base import BaseDriver


class SeleniumDriver(BaseDriver):
    """Selenium backend — prefers undetected-chromedriver, falls back to selenium."""

    def __init__(self, profile) -> None:
        super().__init__(profile)
        self._driver = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> "SeleniumDriver":
        options = self._build_options()
        self._driver = self._create_driver(options)
        self._inject_fingerprint()
        self._started = True
        return self

    def stop(self) -> None:
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
        self._started = False

    def __enter__(self) -> "SeleniumDriver":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Driver + options
    # ------------------------------------------------------------------

    def _build_options(self):
        try:
            import undetected_chromedriver as uc
            options = uc.ChromeOptions()
        except ImportError:
            from selenium.webdriver.chrome.options import Options
            options = Options()

        fp = self.profile.fingerprint

        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={fp.user_agent}")
        options.add_argument(f"--lang={fp.locale}")
        options.add_argument(f"--window-size={fp.resolution_width},{fp.resolution_height}")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        if self.profile.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        if self.profile.data_dir:
            options.add_argument(f"--user-data-dir={self.profile.data_dir}")

        if self.profile.proxy:
            options.add_argument(f"--proxy-server={self.profile.proxy.host}:{self.profile.proxy.port}")

        for arg in self.profile.extra_args:
            options.add_argument(arg)

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        for k, v in self.profile.extra_prefs.items():
            options.add_experimental_option(k, v)

        return options

    def _create_driver(self, options):
        try:
            import undetected_chromedriver as uc
            return uc.Chrome(
                options=options,
                headless=self.profile.headless,
                use_subprocess=True,
            )
        except ImportError:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            return webdriver.Chrome(options=options)

    # ------------------------------------------------------------------
    # Fingerprint injection via CDP + JS
    # ------------------------------------------------------------------

    def _inject_fingerprint(self) -> None:
        fp = self.profile.fingerprint

        try:
            self._driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                "userAgent": fp.user_agent,
                "platform": fp.platform,
                "acceptLanguage": fp.locale,
            })
        except Exception:
            pass

        script = f"""
        Object.defineProperty(navigator, 'platform', {{get: () => '{fp.platform}'}});
        Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {fp.hardware_concurrency}}});
        Object.defineProperty(navigator, 'deviceMemory', {{get: () => {fp.device_memory}}});
        Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
        Object.defineProperty(navigator, 'languages', {{get: () => ['{fp.locale}', 'en']}});
        Object.defineProperty(screen, 'width', {{get: () => {fp.resolution_width}}});
        Object.defineProperty(screen, 'height', {{get: () => {fp.resolution_height}}});
        Object.defineProperty(screen, 'colorDepth', {{get: () => {fp.color_depth}}});
        window.chrome = {{runtime: {{}}, loadTimes: function(){{}}, csi: function(){{}}, app: {{}}}};
        """
        if fp.webgl_vendor:
            script += f"""
        const origGetParam = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {{
            if (p === 37445) return '{fp.webgl_vendor}';
            if (p === 37446) return '{fp.webgl_renderer}';
            return origGetParam.call(this, p);
        }};
            """
        self._driver.execute_script(script)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def get(self, url: str) -> None:
        self._driver.get(url)

    def current_url(self) -> str:
        return self._driver.current_url

    def title(self) -> str:
        return self._driver.title

    def source(self) -> str:
        return self._driver.page_source

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def find(self, selector: str):
        from selenium.webdriver.common.by import By
        return self._driver.find_element(By.CSS_SELECTOR, selector)

    def find_all(self, selector: str):
        from selenium.webdriver.common.by import By
        return self._driver.find_elements(By.CSS_SELECTOR, selector)

    def click(self, selector: str) -> None:
        self.find(selector).click()

    def type(self, selector: str, text: str) -> None:
        from selenium.webdriver.common.keys import Keys
        el = self.find(selector)
        el.clear()
        for char in text:
            el.send_keys(char)
            time.sleep(random.uniform(0.04, 0.12))

    def screenshot(self, path: str) -> None:
        self._driver.save_screenshot(path)

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------

    def get_cookies(self) -> list[dict]:
        return self._driver.get_cookies()

    def set_cookies(self, cookies: list[dict]) -> None:
        for c in cookies:
            try:
                self._driver.add_cookie(c)
            except Exception:
                pass

    def clear_cookies(self) -> None:
        self._driver.delete_all_cookies()

    # ------------------------------------------------------------------
    # JavaScript
    # ------------------------------------------------------------------

    def execute_js(self, script: str, *args) -> Any:
        return self._driver.execute_script(script, *args)

    # ------------------------------------------------------------------
    # Waits
    # ------------------------------------------------------------------

    def wait_for_element(self, selector: str, timeout: float = 10.0):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        return WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    @property
    def driver(self):
        return self._driver
