"""Multilogin X Python SDK — Cloud + Launcher API with Playwright automation.

Partner notes:
  - Multilogin X: code SAAS50 = 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this repo → free tool drops via bot
"""

from mlx.client import MultiloginX
from mlx.constants import AFFILIATE_URL, PARTNER_NOTE, PROMO_CLOUD_PHONE, PROMO_MLX, TELEGRAM_BOT
from mlx.models import AuthTokens, ProfileSession

__all__ = [
    "MultiloginX",
    "AuthTokens",
    "ProfileSession",
    "AFFILIATE_URL",
    "PARTNER_NOTE",
    "PROMO_MLX",
    "PROMO_CLOUD_PHONE",
    "TELEGRAM_BOT",
]
__version__ = "1.5.1"
