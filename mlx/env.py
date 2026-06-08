"""Environment and path helpers for demos and scripts.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def _repo_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "pyproject.toml").exists():
        return candidate
    return Path.cwd()


ROOT = _repo_root()
OUTPUT_DIR = ROOT / "output"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def ensure_output() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def require_env(*keys: str) -> dict[str, str]:
    load_env()
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)} (see .env.example)")
    return {k: os.environ[k] for k in keys}
