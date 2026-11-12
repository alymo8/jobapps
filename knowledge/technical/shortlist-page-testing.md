---
title: Testing the shortlist page locally
status: stable
last_updated: 2026-11-11
sources: the region-neutral shortlist change (ADR 0014)
---

# Testing the shortlist page locally

`templates/shortlist/index.html` can be checked without publishing an artifact.

- **Serve a copy, not the template.** Copy `templates/shortlist/` to a scratch folder, add sample
  week files under `data/` (a `<week>.json` per week and an `index.json` whose `weeks[].json`
  points at them; `latest.json` is the fallback), and serve it with
  `python -m http.server <port> --directory <copy>`. Opening the file directly fails: the page
  `fetch`es its data, which `file://` blocks.
- **No claude.ai runtime is fine.** `claude.use("db")` is absent off claude.ai; the page shows the
  "needs you to be signed in" note and still renders the list, chips and stats. Decision buttons
  and the My decisions tab cannot be tested this way.
- **Switch weeks from script:** set `#weekSel`'s value to a `data/<week>.json` path and call its
  `onchange()`, then read `#stats` and the `.chip` elements.

## Open questions

- None.
