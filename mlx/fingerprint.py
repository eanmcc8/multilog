"""Random fingerprint parameter builders for profile refresh."""
from __future__ import annotations

import random

from mlx.constants import DEFAULT_FLAGS

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

NOISE_OPTIONS = ("mask", "natural", "disabled")


def random_flags() -> dict[str, str]:
    flags = dict(DEFAULT_FLAGS)
    flags["graphics_noise"] = random.choice(NOISE_OPTIONS)
    flags["audio_masking"] = random.choice(NOISE_OPTIONS)
    flags["fonts_masking"] = random.choice(("natural", "mask"))
    flags["navigator_masking"] = "mask"
    return flags


def random_fingerprint_update() -> dict:
    return {
        "parameters": {
            "flags": random_flags(),
            "fingerprint": {
                "navigator": {"user_agent": random.choice(USER_AGENTS)},
            },
        }
    }
