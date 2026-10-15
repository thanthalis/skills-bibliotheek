# -*- coding: utf-8 -*-
"""
marketing-mainframe :: next_period.py

Kijkt naar de laatste run (meest recente snapshot) en stelt de mogelijke
periodes voor de volgende run voor. Print JSON naar stdout.

Output:
{
  "last_run_end": "2026-06-30" | null,     # week_end van de laatste snapshot
  "today": "2026-07-01",
  "recommended": "since_last_run" | "last_7d",
  "since_last_run": {"since","until","days"} | {"status":"none","reason":...},
  "last_7d": {"since","until","days":7}
}

Gebruik:
  - Handmatige run: toon de opties, laat de gebruiker kiezen
    (sinds laatste run / laatste 7 dagen / andere periode).
  - Automatische run (geen mens): neem altijd "since_last_run"; is dat "none",
    dan zijn er geen nieuwe volledige dagen en stop je.

until = gisteren (vandaag is nog niet af; alleen volledige dagen tellen mee).
"""

import json
import glob
import os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP_DIR = os.path.join(HERE, "data", "snapshots")


def latest_week_end():
    ends = []
    for fp in glob.glob(os.path.join(SNAP_DIR, "*.json")):
        try:
            with open(fp, encoding="utf-8") as f:
                snap = json.load(f)
            if snap.get("week_end"):
                ends.append(date.fromisoformat(snap["week_end"]))
        except Exception:
            continue
    return max(ends) if ends else None


def main():
    today = date.today()
    until = today - timedelta(days=1)  # gisteren
    last_end = latest_week_end()

    last7 = {
        "since": (until - timedelta(days=6)).isoformat(),
        "until": until.isoformat(),
        "days": 7,
    }

    if last_end is None:
        since_last = dict(last7)  # geen vorige run: eerste venster = 7 dagen
        recommended = "last_7d"
    else:
        since = last_end + timedelta(days=1)
        if since > until:
            since_last = {"status": "none",
                          "reason": "Geen nieuwe volledige dagen sinds de laatste run (%s)." % last_end.isoformat()}
        else:
            since_last = {"since": since.isoformat(), "until": until.isoformat(),
                          "days": (until - since).days + 1}
        recommended = "since_last_run"

    print(json.dumps({
        "last_run_end": last_end.isoformat() if last_end else None,
        "today": today.isoformat(),
        "recommended": recommended,
        "since_last_run": since_last,
        "last_7d": last7,
    }, indent=2))


if __name__ == "__main__":
    main()
