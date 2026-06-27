"""Anti-bot profile presets for scraping (DataDome, Akamai).
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""

from __future__ import annotations

import copy

from mlx.constants import DEFAULT_FLAGS, QUICK_PROFILE_DEFAULTS

STRICT_FLAGS = copy.deepcopy(DEFAULT_FLAGS)
STRICT_FLAGS.update(
    {
        "audio_masking": "mask",
        "fonts_masking": "mask",
        "graphics_masking": "mask",
        "graphics_noise": "mask",
        "navigator_masking": "mask",
        "webrtc_masking": "mask",
        "proxy_masking": "mask",
    }
)


def antibot_profile_parameters(*, strict: bool = True) -> dict:
    flags = STRICT_FLAGS if strict else DEFAULT_FLAGS
    return {
        "flags": flags,
        "storage": QUICK_PROFILE_DEFAULTS["parameters"]["storage"],
    }


def antibot_quick_payload(**overrides) -> dict:
    payload = copy.deepcopy(QUICK_PROFILE_DEFAULTS)
    payload["parameters"] = antibot_profile_parameters(strict=True)
    payload.update(overrides)
    return payload
