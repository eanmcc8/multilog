"""Farm — run any task across many profiles in parallel or sequentially.

Works with all three backends.

Sync example (Selenium / HTTP):
    profiles = BrowserProfile.batch(10, driver="http")
    farm = Farm(profiles)
    results = farm.run(my_task_fn, delay=1.0)

Async example (Playwright):
    profiles = BrowserProfile.batch(5, driver="playwright")
    farm = Farm(profiles)
    results = asyncio.run(farm.run_async(my_async_task_fn, concurrency=3))
"""
from __future__ import annotations

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable

from stealthbrowser.profile import BrowserProfile
from stealthbrowser.session import StealthSession


@dataclass
class FarmResult:
    profile_name: str
    profile_id: str
    status: str          # "ok" | "fail" | "skip"
    data: Any = None
    error: str = ""
    elapsed: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status == "ok"


class Farm:
    """Orchestrate a task across multiple profiles."""

    def __init__(self, profiles: list[BrowserProfile]) -> None:
        self.profiles = profiles

    # ------------------------------------------------------------------
    # Sync runner (Selenium / HTTP — uses threads)
    # ------------------------------------------------------------------

    def run(
        self,
        task: Callable[[StealthSession, BrowserProfile], Any],
        *,
        delay: float = 0.0,
        max_workers: int = 1,
        stop_on_fail: bool = False,
        verbose: bool = True,
    ) -> list[FarmResult]:
        """Run *task(session, profile)* for every profile.

        task receives an already-started StealthSession and the profile.
        Set max_workers > 1 for parallel execution (HTTP driver only — Chrome
        drivers are not thread-safe when sharing a single process).
        """
        results: list[FarmResult] = []

        def _run_one(profile: BrowserProfile) -> FarmResult:
            t0 = time.monotonic()
            try:
                with StealthSession(profile) as session:
                    data = task(session, profile)
                elapsed = time.monotonic() - t0
                if verbose:
                    print(f"  [OK]   {profile.name} ({elapsed:.1f}s)")
                return FarmResult(profile.name, profile.id, "ok", data=data, elapsed=elapsed)
            except Exception as exc:
                elapsed = time.monotonic() - t0
                if verbose:
                    print(f"  [FAIL] {profile.name}: {exc}")
                return FarmResult(profile.name, profile.id, "fail", error=str(exc), elapsed=elapsed)

        if max_workers <= 1:
            for i, profile in enumerate(self.profiles, 1):
                if verbose:
                    print(f"\n[{i}/{len(self.profiles)}] {profile.name} ({profile.driver})")
                result = _run_one(profile)
                results.append(result)
                if stop_on_fail and not result.ok:
                    break
                if delay and i < len(self.profiles):
                    time.sleep(delay)
        else:
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = {pool.submit(_run_one, p): p for p in self.profiles}
                for future in as_completed(futures):
                    results.append(future.result())

        return results

    # ------------------------------------------------------------------
    # Async runner (Playwright — uses asyncio semaphore for concurrency)
    # ------------------------------------------------------------------

    async def run_async(
        self,
        task: Callable,
        *,
        concurrency: int = 1,
        delay: float = 0.0,
        stop_on_fail: bool = False,
        verbose: bool = True,
    ) -> list[FarmResult]:
        """Run *async task(session, profile)* across all profiles.

        concurrency controls how many Playwright sessions run simultaneously.
        """
        sem = asyncio.Semaphore(concurrency)
        results: list[FarmResult] = []

        async def _run_one(profile: BrowserProfile, idx: int) -> FarmResult:
            async with sem:
                if verbose:
                    print(f"\n[{idx}/{len(self.profiles)}] {profile.name} (playwright)")
                t0 = asyncio.get_event_loop().time()
                try:
                    async with StealthSession(profile) as session:
                        data = await task(session, profile)
                    elapsed = asyncio.get_event_loop().time() - t0
                    if verbose:
                        print(f"  [OK]   {profile.name} ({elapsed:.1f}s)")
                    return FarmResult(profile.name, profile.id, "ok", data=data, elapsed=elapsed)
                except Exception as exc:
                    elapsed = asyncio.get_event_loop().time() - t0
                    if verbose:
                        print(f"  [FAIL] {profile.name}: {exc}")
                    return FarmResult(profile.name, profile.id, "fail", error=str(exc), elapsed=elapsed)

        tasks = [_run_one(p, i + 1) for i, p in enumerate(self.profiles)]
        for result in await asyncio.gather(*tasks):
            results.append(result)
            if stop_on_fail and not result.ok:
                break
            if delay:
                await asyncio.sleep(delay)

        return results

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    @staticmethod
    def summarize(results: list[FarmResult], *, verbose: bool = True) -> dict:
        ok = [r for r in results if r.ok]
        fail = [r for r in results if not r.ok]
        summary = {
            "total": len(results),
            "ok": len(ok),
            "fail": len(fail),
            "avg_elapsed": round(sum(r.elapsed for r in results) / max(len(results), 1), 2),
            "errors": {r.profile_name: r.error for r in fail},
        }
        if verbose:
            print(f"\n--- Farm Summary ---")
            print(f"  Total : {summary['total']}")
            print(f"  OK    : {summary['ok']}")
            print(f"  Failed: {summary['fail']}")
            print(f"  Avg   : {summary['avg_elapsed']}s")
        return summary
