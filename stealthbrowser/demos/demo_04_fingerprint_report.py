"""Demo 04 — Show a detailed fingerprint report for each OS type."""
from __future__ import annotations

import json

from stealthbrowser.profile import BrowserProfile, Fingerprint

for os_name in ("windows", "macos", "linux"):
    p = BrowserProfile.random(os=os_name, driver="http")
    fp = p.fingerprint
    report = {
        "os": os_name,
        "name": p.name,
        "user_agent": fp.user_agent,
        "platform": fp.platform,
        "resolution": f"{fp.resolution_width}x{fp.resolution_height}",
        "pixel_ratio": fp.pixel_ratio,
        "locale": fp.locale,
        "timezone": fp.timezone,
        "hardware_concurrency": fp.hardware_concurrency,
        "device_memory": fp.device_memory,
        "webgl_vendor": fp.webgl_vendor,
        "webgl_renderer": fp.webgl_renderer,
        "canvas_noise": fp.canvas_noise,
        "audio_noise": fp.audio_noise,
        "do_not_track": fp.do_not_track,
        "fonts_count": len(fp.fonts),
    }
    print(json.dumps(report, indent=2))
    print()
