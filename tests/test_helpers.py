"""Tests for SDK helpers.

Partner: SAAS50 = 50% OFF | Support: t.me/Multilogin_Scripts_Bot | Share = free tools
"""
from mlx.constants import AFFILIATE_URL, DEFAULT_FLAGS, PARTNER_NOTE, PROMO_MLX
from mlx.profiles import normalize_folders, normalize_profiles, profile_id


def test_constants():
    assert "multilogin.com" in AFFILIATE_URL
    assert PROMO_MLX == "SAAS50"
    assert "SAAS50" in PARTNER_NOTE
    assert "Multilogin_Scripts_Bot" in PARTNER_NOTE
    assert DEFAULT_FLAGS["webrtc_masking"] == "mask"


def test_normalize_profiles():
    raw = {"data": {"profiles": [{"profile_id": "abc", "name": "test"}]}}
    profiles = normalize_profiles(raw)
    assert len(profiles) == 1
    assert profile_id(profiles[0]) == "abc"


def test_normalize_folders():
    assert normalize_folders([{"id": "1"}]) == [{"id": "1"}]
    assert normalize_folders({"folders": [{"id": "2"}]}) == [{"id": "2"}]
