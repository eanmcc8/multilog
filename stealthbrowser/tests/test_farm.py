"""Tests for Farm — using the HTTP driver so no browser is needed."""
from __future__ import annotations

import pytest

from stealthbrowser.farm import Farm, FarmResult
from stealthbrowser.profile import BrowserProfile
from stealthbrowser.session import StealthSession


def _profiles(n: int = 3) -> list[BrowserProfile]:
    return BrowserProfile.batch(n, driver="http", name_prefix="Test")


def test_farm_basic():
    def task(session: StealthSession, profile: BrowserProfile):
        session.get("https://httpbin.org/get")
        return session.status_code()

    profiles = _profiles(2)
    farm = Farm(profiles)
    results = farm.run(task, verbose=False)
    assert len(results) == 2
    for r in results:
        assert r.ok
        assert r.data == 200


def test_farm_result_fields():
    def task(session, profile):
        return {"name": profile.name}

    profiles = _profiles(1)
    results = Farm(profiles).run(task, verbose=False)
    r = results[0]
    assert isinstance(r, FarmResult)
    assert r.profile_name
    assert r.profile_id
    assert r.status == "ok"
    assert r.elapsed >= 0


def test_farm_handles_failure():
    def task(session, profile):
        raise ValueError("intentional failure")

    profiles = _profiles(2)
    results = Farm(profiles).run(task, verbose=False)
    assert all(r.status == "fail" for r in results)
    assert all("intentional failure" in r.error for r in results)


def test_farm_stop_on_fail():
    calls = []

    def task(session, profile):
        calls.append(profile.name)
        raise RuntimeError("stop")

    profiles = _profiles(3)
    results = Farm(profiles).run(task, verbose=False, stop_on_fail=True)
    assert len(results) == 1
    assert len(calls) == 1


def test_farm_summarize():
    results = [
        FarmResult("a", "id1", "ok", elapsed=1.0),
        FarmResult("b", "id2", "fail", error="oops", elapsed=2.0),
    ]
    summary = Farm.summarize(results, verbose=False)
    assert summary["total"] == 2
    assert summary["ok"] == 1
    assert summary["fail"] == 1
    assert "b" in summary["errors"]
