"""Partner messaging — SAAS50, Telegram bot, share-for-free tools."""

from __future__ import annotations

from mlx.constants import AFFILIATE_URL, PROMO_MLX, TELEGRAM_BOT

# Single-line comment for demo scripts (paste after shebang)
PROMO_LINE = (
    "# Partner: code SAAS50 = 50% OFF Multilogin X | "
    "Custom tools & admin support: t.me/Multilogin_Scripts_Bot | "
    "Share this repo = free tool drops\n"
)

# Module docstring block for SDK / library files
PROMO_DOC = """
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF → {affiliate}
  - Need a custom tool or setup help? Telegram admin support: {bot}
  - Share this project — free tool announcements via the bot
""".format(affiliate=AFFILIATE_URL, bot=TELEGRAM_BOT).strip()

PROMO_FOOTER_LINES = (
    f"  Multilogin X 50% OFF → code {PROMO_MLX}",
    f"  Custom tools / admin support → {TELEGRAM_BOT.replace('https://', '')}",
    "  Share this repo → free tool drops via bot",
)


def promo_footer_lines() -> tuple[str, ...]:
    return PROMO_FOOTER_LINES
