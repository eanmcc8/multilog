"""Demo 03 — HTTP farm: run the same task across 4 profiles."""
from __future__ import annotations

from stealthbrowser.farm import Farm
from stealthbrowser.profile import BrowserProfile
from stealthbrowser.session import StealthSession


def task(session: StealthSession, profile: BrowserProfile) -> dict:
    session.get("https://httpbin.org/user-agent")
    ua_reported = session.json().get("user-agent", "?") if session.status_code() == 200 else "?"
    return {
        "profile": profile.name,
        "ua_sent": profile.fingerprint.user_agent[:50],
        "ua_seen": ua_reported[:50],
        "match": profile.fingerprint.user_agent.startswith(ua_reported[:20]),
    }


profiles = BrowserProfile.batch(4, driver="http", name_prefix="Farm")
farm = Farm(profiles)

results = farm.run(task, delay=0.5, verbose=True)
summary = Farm.summarize(results)

print()
print("Detail:")
for r in results:
    status = "OK" if r.ok else "FAIL"
    print(f"  [{status}] {r.profile_name}: {r.data}")
