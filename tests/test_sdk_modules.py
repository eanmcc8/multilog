"""Partner notes:
  - Multilogin X: use code SAAS50 for 50% OFF
  - Custom tools / admin support: https://t.me/Multilogin_Scripts_Bot
  - Share this project to get free tool announcements via the bot"""
from pathlib import Path

from mlx.antibot import antibot_profile_parameters
from mlx.cookies import load_cookies, parse_netscape, to_netscape
from mlx.farm import BUILTIN_TASKS, demo_script
from mlx.proxy_utils import parse_proxy, proxy_payload


def test_parse_proxy():
    assert parse_proxy("127.0.0.1:8080") == ("127.0.0.1", 8080, "http", "", "")
    assert parse_proxy("socks5://host:1080:user:pass") == ("host", 1080, "socks5", "user", "pass")
    assert parse_proxy("# comment") is None


def test_proxy_payload():
    p = proxy_payload("1.2.3.4", 3128, "http", "u", "p")
    assert p["host"] == "1.2.3.4"
    assert p["username"] == "u"


def test_netscape_roundtrip():
    raw = "# Netscape\n.example.com\tTRUE\t/\tFALSE\t0\tsid\tabc\n"
    cookies = parse_netscape(raw)
    assert len(cookies) == 1
    assert cookies[0]["name"] == "sid"
    out = to_netscape(cookies)
    assert "sid\tabc" in out


def test_load_json_cookies(tmp_path: Path):
    f = tmp_path / "c.json"
    f.write_text('[{"domain":".x.com","name":"a","value":"1","path":"/"}]', encoding="utf-8")
    cookies = load_cookies(f)
    assert len(cookies) == 1


def test_antibot_flags():
    params = antibot_profile_parameters(strict=True)
    assert params["flags"]["navigator_masking"] == "mask"


def test_demo_script_lookup():
    p = demo_script("01")
    assert p is not None
    assert p.name.startswith("01_")


def test_builtin_tasks():
    assert "google" in BUILTIN_TASKS
    assert "trustpilot" in BUILTIN_TASKS
