"""Profile helper utilities.
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

from typing import Any


def normalize_folders(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        return raw.get("folders", [raw])
    return []


def normalize_profiles(search_result: dict[str, Any]) -> list[dict[str, Any]]:
    data = search_result.get("data", search_result)
    if isinstance(data, list):
        return data
    return data.get("profiles", [])


def profile_id(profile: dict[str, Any]) -> str:
    return profile.get("profile_id") or profile.get("id") or ""


def folder_id(profile: dict[str, Any], fallback: str = "") -> str:
    return profile.get("folder_id") or fallback
