"""
Multilogin X full API client.
Cloud API: https://api.multilogin.com
Launcher API: https://launcher.mlx.yt:45001
Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot
"""
from __future__ import annotations

import os
import time
from typing import Any, Literal

import requests
from dotenv import load_dotenv

from mlx.constants import DEFAULT_FLAGS, QUICK_PROFILE_DEFAULTS
from mlx.exceptions import MLXAPIError, MLXAuthError
from mlx.models import AuthTokens, ProfileSession

load_dotenv()

AutomationType = Literal["selenium", "puppeteer", "playwright"]


class MultiloginX:
    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        *,
        cloud_url: str | None = None,
        launcher_url: str | None = None,
        token: str | None = None,
        refresh_token: str | None = None,
    ):
        self.email = email or os.getenv("MLX_EMAIL", "")
        self.password = password or os.getenv("MLX_PASSWORD", "")
        self.cloud_url = (cloud_url or os.getenv("MLX_CLOUD_URL", "https://api.multilogin.com")).rstrip("/")
        self.launcher_url = (
            launcher_url or os.getenv("MLX_LAUNCHER_URL", "https://launcher.mlx.yt:45001")
        ).rstrip("/")
        self._token = token or os.getenv("MLX_TOKEN")
        self._refresh_token = refresh_token or os.getenv("MLX_REFRESH_TOKEN", "")
        self._token_expires_at = 0.0

    # ------------------------------------------------------------------ HTTP
    @property
    def headers(self) -> dict[str, str]:
        self._ensure_token()
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _ensure_token(self) -> None:
        if self._token and time.time() < self._token_expires_at:
            return
        if self._token and self._refresh_token:
            try:
                self.refresh_token()
                return
            except MLXAPIError:
                pass
        if not self.email or not self.password:
            raise MLXAuthError("MLX_EMAIL / MLX_PASSWORD or MLX_TOKEN required")
        self.sign_in()

    def _request(
        self,
        method: str,
        url: str,
        *,
        auth: bool = True,
        json_body: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        hdrs = self.headers if auth else {"Accept": "application/json", "Content-Type": "application/json"}
        resp = requests.request(method, url, headers=hdrs, json=json_body, params=params, timeout=timeout)
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text}
        if resp.status_code >= 400:
            msg = body.get("status", {}).get("message") or body.get("message") or resp.text
            raise MLXAPIError(str(msg), resp.status_code, body)
        status = body.get("status", {})
        if status.get("error_code"):
            raise MLXAPIError(status.get("message", "API error"), resp.status_code, body)
        return body

    def _cloud(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        return self._request(method, f"{self.cloud_url}{path}", **kwargs)

    def _launcher(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        return self._request(method, f"{self.launcher_url}{path}", **kwargs)

    # ------------------------------------------------------------------ Auth
    def sign_in(self) -> AuthTokens:
        body = self._cloud(
            "POST",
            "/user/signin",
            auth=False,
            json_body={"email": self.email, "password": self.password},
        )
        data = body["data"]
        self._token = data["token"]
        self._refresh_token = data.get("refresh_token", "")
        self._token_expires_at = time.time() + 25 * 60
        return AuthTokens(
            token=self._token,
            refresh_token=self._refresh_token,
            user_id=data.get("user_id", ""),
            workspace_id=data.get("workspace_id", ""),
        )

    def refresh_token(self, workspace_id: str | None = None) -> AuthTokens:
        payload: dict[str, Any] = {"refresh_token": self._refresh_token}
        if workspace_id:
            payload["workspace_id"] = workspace_id
        body = self._cloud("POST", "/user/refresh_token", json_body=payload)
        data = body["data"]
        self._token = data["token"]
        self._refresh_token = data.get("refresh_token", self._refresh_token)
        self._token_expires_at = time.time() + 25 * 60
        return AuthTokens(
            token=self._token,
            refresh_token=self._refresh_token,
            workspace_id=data.get("workspace_id", ""),
        )

    # ---------------------------------------------------------------- Workspace
    def get_folders(self) -> list[dict[str, Any]]:
        body = self._cloud("GET", "/workspace/folders")
        return body.get("data", body if isinstance(body, list) else [])

    def get_workspaces(self) -> list[dict[str, Any]]:
        body = self._cloud("GET", "/user/workspaces")
        return body.get("data", [])

    # ---------------------------------------------------------------- Profiles (cloud)
    def search_profiles(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        search_text: str = "",
        folder_id: str = "",
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"limit": limit, "offset": offset}
        if search_text:
            payload["search_text"] = search_text
        if folder_id:
            payload["folder_id"] = folder_id
        return self._cloud("POST", "/profile/search", json_body=payload)

    def create_profile(self, name: str, folder_id: str, **kwargs) -> dict[str, Any]:
        payload = {
            "name": name,
            "folder_id": folder_id,
            "browser_type": kwargs.get("browser_type", "mimic"),
            "os_type": kwargs.get("os_type", "windows"),
            "parameters": kwargs.get("parameters", {"flags": dict(DEFAULT_FLAGS)}),
        }
        return self._cloud("POST", "/profile/create", json_body=payload)

    def remove_profiles(self, profile_ids: list[str]) -> dict[str, Any]:
        return self._cloud("POST", "/profile/remove", json_body={"profile_ids": profile_ids})

    def clone_profile(self, profile_id: str, folder_id: str, name: str) -> dict[str, Any]:
        return self._cloud(
            "POST",
            "/profile/clone",
            json_body={"profile_id": profile_id, "folder_id": folder_id, "name": name},
        )

    def update_profile(self, profile_id: str, **fields) -> dict[str, Any]:
        payload = {"profile_id": profile_id, **fields}
        return self._cloud("POST", "/profile/update", json_body=payload)

    def generate_proxy(self, country: str = "us", session_type: str = "sticky") -> dict[str, Any]:
        return self._cloud(
            "POST",
            "/proxy/generate",
            json_body={"country": country, "session_type": session_type},
        )

    def get_profile_summary(self) -> dict[str, Any]:
        return self._cloud("GET", "/profile/summary")

    # ---------------------------------------------------------------- Launcher
    def start_profile(
        self,
        profile_id: str,
        folder_id: str,
        *,
        automation_type: AutomationType = "playwright",
        headless: bool = False,
        strict_mode: bool = False,
    ) -> ProfileSession:
        params = {
            "automation_type": automation_type,
            "headless_mode": str(headless).lower(),
        }
        hdrs = self.headers.copy()
        if strict_mode:
            hdrs["X-Strict-Mode"] = "true"
        url = f"{self.launcher_url}/api/v2/profile/f/{folder_id}/p/{profile_id}/start"
        resp = requests.get(url, headers=hdrs, params=params, timeout=90)
        body = resp.json()
        if resp.status_code >= 400:
            raise MLXAPIError(body.get("status", {}).get("message", resp.text), resp.status_code, body)
        return ProfileSession.from_start_response(folder_id, profile_id, body["data"])

    def stop_profile(self, profile_id: str, folder_id: str | None = None) -> dict[str, Any]:
        if folder_id:
            return self._launcher(
                "GET",
                f"/api/v2/profile/f/{folder_id}/p/{profile_id}/stop",
            )
        return self._launcher("GET", "/api/v1/profile/stop", params={"profile_id": profile_id})

    def stop_all_profiles(self) -> dict[str, Any]:
        return self._launcher("GET", "/api/v1/profile/stop_all")

    def get_active_profiles(self) -> dict[str, Any]:
        return self._launcher("GET", "/api/v2/profile/active")

    def start_quick_profile(self, payload: dict[str, Any]) -> ProfileSession:
        body = self._launcher("POST", "/api/v3/profile/quick", json_body=payload)
        data = body["data"]
        return ProfileSession.from_start_response("", data["id"], data)

    # ---------------------------------------------------------------- Proxy & cookies
    def validate_proxy(
        self, host: str, port: int, proxy_type: str = "http", username: str = "", password: str = ""
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"host": host, "type": proxy_type, "port": port}
        if username:
            payload["username"] = username
            payload["password"] = password
        return self._launcher("POST", "/api/v1/proxy/validate", json_body=payload)

    def import_cookies(self, profile_id: str, cookies: list[dict]) -> dict[str, Any]:
        return self._launcher(
            "POST",
            "/api/v1/cookies/import",
            json_body={"profile_id": profile_id, "cookies": cookies},
        )

    def export_cookies(self, profile_id: str) -> dict[str, Any]:
        return self._launcher(
            "POST",
            "/api/v1/cookies/export",
            json_body={"profile_id": profile_id},
        )

    def build_quick_profile_payload(self, **overrides) -> dict[str, Any]:
        """Build a v3 quick-profile payload with sensible defaults."""
        import copy

        payload = copy.deepcopy(QUICK_PROFILE_DEFAULTS)
        for key, value in overrides.items():
            if key == "parameters" and isinstance(value, dict):
                payload["parameters"].update(value)
            else:
                payload[key] = value
        payload.setdefault("automation", "playwright")
        return payload

    def move_profiles(self, profile_ids: list[str], folder_id: str) -> dict[str, Any]:
        return self._cloud(
            "POST",
            "/profile/move",
            json_body={"profile_ids": profile_ids, "folder_id": folder_id},
        )

    def get_launcher_version(self) -> dict[str, Any]:
        return self._launcher("GET", "/api/v1/version", auth=False)


__all__ = ["MultiloginX", "AutomationType"]
