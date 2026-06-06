from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class AuthTokens:
    token: str
    refresh_token: str = ""
    user_id: str = ""
    workspace_id: str = ""


@dataclass
class ProfileSession:
    profile_id: str
    folder_id: str
    port: str
    browser_url: str
    is_quick: bool = False
    browser_type: str = ""
    core_version: int | None = None

    @classmethod
    def from_start_response(
        cls, folder_id: str, profile_id: str, data: dict[str, Any]
    ) -> ProfileSession:
        port = str(data["port"])
        return cls(
            profile_id=data.get("id", profile_id),
            folder_id=folder_id,
            port=port,
            browser_url=f"http://127.0.0.1:{port}",
            is_quick=bool(data.get("is_quick")),
            browser_type=data.get("browser_type", ""),
            core_version=data.get("core_version"),
        )
