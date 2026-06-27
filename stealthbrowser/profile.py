"""BrowserProfile — fully customizable local fingerprint profiles.

No external service required.  Everything is defined locally and serialized
to / from plain dicts so profiles can be stored as JSON files.
"""
from __future__ import annotations

import json
import random
import string
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

OS = Literal["windows", "macos", "linux"]
DRIVER = Literal["playwright", "selenium", "http"]

# ---------------------------------------------------------------------------
# Fingerprint data pools
# ---------------------------------------------------------------------------

_UA_POOL: dict[str, list[str]] = {
    "windows": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    ],
    "macos": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    ],
    "linux": [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    ],
}

_RESOLUTIONS = [
    (1920, 1080), (1366, 768), (1536, 864), (1440, 900),
    (1280, 720), (1600, 900), (2560, 1440), (1280, 800),
]

_LOCALES = ["en-US", "en-GB", "de-DE", "fr-FR", "es-ES", "pt-BR", "ja-JP", "zh-CN"]

_TIMEZONES = [
    "America/New_York", "America/Chicago", "America/Los_Angeles", "America/Denver",
    "Europe/London", "Europe/Berlin", "Europe/Paris", "Asia/Tokyo",
    "Asia/Shanghai", "Australia/Sydney", "America/Sao_Paulo",
]

_PLATFORMS: dict[str, str] = {
    "windows": "Win32",
    "macos": "MacIntel",
    "linux": "Linux x86_64",
}

_WEBGL_VENDORS = [
    ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0)"),
    ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)"),
    ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)"),
    ("Apple", "Apple M1"),
    ("Mesa/X.org", "Mesa DRI Intel(R) UHD Graphics 630"),
]

_FONT_SETS: dict[str, list[str]] = {
    "windows": ["Arial", "Times New Roman", "Verdana", "Georgia", "Courier New",
                "Trebuchet MS", "Impact", "Comic Sans MS", "Tahoma", "Calibri"],
    "macos": ["Helvetica", "Times New Roman", "Verdana", "Georgia", "Courier New",
              "Trebuchet MS", "Futura", "Gill Sans", "Arial", "Palatino"],
    "linux": ["DejaVu Sans", "FreeSans", "Liberation Sans", "Ubuntu", "Cantarell",
              "Noto Sans", "Droid Sans", "Arial", "Verdana", "Times New Roman"],
}


# ---------------------------------------------------------------------------
# Proxy config
# ---------------------------------------------------------------------------

@dataclass
class ProxyConfig:
    host: str
    port: int
    type: Literal["http", "https", "socks5"] = "http"
    username: str = ""
    password: str = ""

    @classmethod
    def from_string(cls, line: str) -> "ProxyConfig":
        """Parse proxy strings in any common format:
          - host:port
          - host:port:user:pass
          - type://host:port
          - type://user:pass@host:port
          - type://host:port:user:pass
        """
        line = line.strip()
        ptype = "http"
        if "://" in line:
            ptype, line = line.split("://", 1)
        user = ""
        pwd = ""
        if "@" in line:
            auth, line = line.rsplit("@", 1)
            if ":" in auth:
                user, pwd = auth.split(":", 1)
            else:
                user = auth
        parts = line.split(":")
        host = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 8080
        if not user and len(parts) > 2:
            user = parts[2]
        if not pwd and len(parts) > 3:
            pwd = parts[3]
        return cls(host=host, port=port, type=ptype.lower(), username=user, password=pwd)

    @property
    def url(self) -> str:
        auth = f"{self.username}:{self.password}@" if self.username else ""
        return f"{self.type}://{auth}{self.host}:{self.port}"

    def as_playwright_dict(self) -> dict:
        d: dict = {"server": f"{self.type}://{self.host}:{self.port}"}
        if self.username:
            d["username"] = self.username
            d["password"] = self.password
        return d

    def as_selenium_dict(self) -> dict:
        return {"proxyType": "manual", "httpProxy": f"{self.host}:{self.port}",
                "sslProxy": f"{self.host}:{self.port}"}


# ---------------------------------------------------------------------------
# Fingerprint
# ---------------------------------------------------------------------------

@dataclass
class Fingerprint:
    user_agent: str = ""
    platform: str = ""
    vendor: str = "Google Inc."
    webgl_vendor: str = ""
    webgl_renderer: str = ""
    resolution_width: int = 1920
    resolution_height: int = 1080
    color_depth: int = 24
    pixel_ratio: float = 1.0
    locale: str = "en-US"
    timezone: str = "America/New_York"
    fonts: list[str] = field(default_factory=list)
    do_not_track: bool = False
    hardware_concurrency: int = 4
    device_memory: int = 8
    canvas_noise: float = 0.0
    audio_noise: float = 0.0

    @classmethod
    def random(cls, os: OS = "windows") -> "Fingerprint":
        wv, wr = random.choice(_WEBGL_VENDORS)
        w, h = random.choice(_RESOLUTIONS)
        return cls(
            user_agent=random.choice(_UA_POOL.get(os, _UA_POOL["windows"])),
            platform=_PLATFORMS.get(os, "Win32"),
            webgl_vendor=wv,
            webgl_renderer=wr,
            resolution_width=w,
            resolution_height=h,
            color_depth=random.choice([24, 30]),
            pixel_ratio=random.choice([1.0, 1.25, 1.5, 2.0]),
            locale=random.choice(_LOCALES),
            timezone=random.choice(_TIMEZONES),
            fonts=random.sample(_FONT_SETS.get(os, _FONT_SETS["windows"]), k=random.randint(5, 9)),
            do_not_track=random.random() < 0.2,
            hardware_concurrency=random.choice([2, 4, 6, 8, 12, 16]),
            device_memory=random.choice([2, 4, 8, 16, 32]),
            canvas_noise=round(random.uniform(0.001, 0.01), 4),
            audio_noise=round(random.uniform(0.0001, 0.001), 5),
        )


# ---------------------------------------------------------------------------
# BrowserProfile
# ---------------------------------------------------------------------------

@dataclass
class BrowserProfile:
    """A fully self-contained browser identity — no external service needed."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    os: OS = "windows"
    driver: DRIVER = "playwright"
    headless: bool = False
    fingerprint: Fingerprint = field(default_factory=Fingerprint.random)
    proxy: ProxyConfig | None = None

    # Extra browser flags / prefs (driver-specific, passed through as-is)
    extra_args: list[str] = field(default_factory=list)
    extra_prefs: dict[str, Any] = field(default_factory=dict)

    # Persistent storage path — if set, browser reuses this profile directory
    data_dir: str = ""

    # Tags for grouping / filtering
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.name = f"Profile-{suffix}"
        if isinstance(self.fingerprint, dict):
            self.fingerprint = Fingerprint(**self.fingerprint)
        if isinstance(self.proxy, dict):
            self.proxy = ProxyConfig(**self.proxy)

    # ------------------------------------------------------------------
    # Randomization helpers
    # ------------------------------------------------------------------

    def randomize_fingerprint(self) -> "BrowserProfile":
        """Replace fingerprint with a fresh random one (keeps same OS)."""
        self.fingerprint = Fingerprint.random(self.os)
        return self

    def rotate_proxy(self, proxies: list[str]) -> "BrowserProfile":
        """Pick a random proxy from a list of proxy strings."""
        if proxies:
            self.proxy = ProxyConfig.from_string(random.choice(proxies))
        return self

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "BrowserProfile":
        fp_data = data.pop("fingerprint", {})
        proxy_data = data.pop("proxy", None)
        obj = cls(**data)
        obj.fingerprint = Fingerprint(**fp_data) if fp_data else Fingerprint.random(obj.os)
        obj.proxy = ProxyConfig(**proxy_data) if proxy_data else None
        return obj

    @classmethod
    def from_json(cls, text: str) -> "BrowserProfile":
        return cls.from_dict(json.loads(text))

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json())
        return p

    @classmethod
    def load(cls, path: str | Path) -> "BrowserProfile":
        return cls.from_json(Path(path).read_text())

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    @classmethod
    def random(
        cls,
        *,
        os: OS = "windows",
        driver: DRIVER = "playwright",
        proxy: str | None = None,
        headless: bool = False,
        name: str = "",
    ) -> "BrowserProfile":
        """Create a ready-to-use profile with randomized fingerprint."""
        p = cls(
            os=os,
            driver=driver,
            headless=headless,
            name=name,
            fingerprint=Fingerprint.random(os),
        )
        if proxy:
            p.proxy = ProxyConfig.from_string(proxy)
        return p

    @classmethod
    def batch(
        cls,
        count: int,
        *,
        os: OS = "windows",
        driver: DRIVER = "playwright",
        proxies: list[str] | None = None,
        headless: bool = False,
        name_prefix: str = "Profile",
    ) -> list["BrowserProfile"]:
        """Create `count` randomized profiles, optionally cycling through proxies."""
        profiles = []
        for i in range(count):
            p = cls.random(os=os, driver=driver, headless=headless, name=f"{name_prefix}-{i+1:03d}")
            if proxies:
                p.proxy = ProxyConfig.from_string(proxies[i % len(proxies)])
            profiles.append(p)
        return profiles
