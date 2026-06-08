"""Shared constants and partner links.

Partner notes:
  - Multilogin X: code SAAS50 = 50% OFF first order
  - Custom tool requests / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to receive free tool announcements via the bot
"""

AFFILIATE_URL = "https://multilogin.com?a_aid=saas"
PROMO_MLX = "SAAS50"
PROMO_CLOUD_PHONE = "MIN50"
TELEGRAM_BOT = "https://t.me/Multilogin_Scripts_Bot"
PARTNER_NOTE = (
    f"Multilogin X 50% OFF with code {PROMO_MLX} | "
    f"Custom tools & support: {TELEGRAM_BOT} | Share = free tools"
)

DEFAULT_FLAGS = {
    "audio_masking": "mask",
    "fonts_masking": "natural",
    "geolocation_masking": "mask",
    "geolocation_popup": "prompt",
    "graphics_masking": "mask",
    "graphics_noise": "mask",
    "localization_masking": "mask",
    "media_devices_masking": "natural",
    "navigator_masking": "mask",
    "ports_masking": "mask",
    "proxy_masking": "disabled",
    "screen_masking": "mask",
    "timezone_masking": "mask",
    "webrtc_masking": "mask",
}

QUICK_PROFILE_DEFAULTS = {
    "browser_type": "mimic",
    "os_type": "windows",
    "is_headless": False,
    "parameters": {
        "flags": DEFAULT_FLAGS,
        "storage": {
            "bookmarks": True,
            "cookies": True,
            "extensions": True,
            "history": True,
            "local_storage": True,
            "passwords": True,
        },
    },
}
