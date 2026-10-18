# Gate: Job shortlist skill: design

- **Spec:** docs/superpowers/specs/2026-10-18-job-shortlist-design.md
- **Spec SHA-256:** 98e73f26686897a3d165596b7eb63e95c3984a1f1333f56cf6a9bb3a2bac1b89
- **Verdict:** pass
- **Date:** 2026-10-18
- **Rounds:** 2 discovery + 0 verification

## Key decisions

- The skill and a tested stdlib helper live in this repo (`.claude/skills/job-shortlist/`, `tools/shortlist.py`), not as a user-level skill; the repo is private, so the artifact URL is written in it.
- Claude Code writes only to the artifact's `decisions` collection and never publishes or changes the page, its capabilities or `data/*`; nothing on the claude.ai side changes.
- Keys come only from the downloaded `decision_keys.py`, imported by path and run with `python -I`, cached at `~/.job-shortlist/decision_keys.py`; a byte-for-byte fixture copy is used by tests only.
- A posting counts as decided when `url_norm` OR `match_key` matches, the weekly run's rule.
- The "Mark as applied?" hook runs at four points: `/apply` after submit, `/resume` and `/cover-letter` when run directly, `/batch` once at finish; the claude.ai skills `tailor-resume` and `write-cover-letter` get paste-in lines only.
- Not-interested writes need Aly's OK above 3 postings; 3 or fewer are written directly.
- Pending fallback: `~/.job-shortlist/pending-decisions.jsonl`, with keys recomputed at flush when no cache existed; cleared only after every write succeeded.
- The skill does not write `applications.md`.
- ADR 0004 records the artifact as the shortlist data store; the CLAUDE.md sentence is narrowed to "of the six source Docs"; ADR 0003 is not changed.
- No real decision is written during implementation or testing.

## Findings fixed

- round 1 [blocking] No ADR for adopting the shortlist artifact as an external data store: added ADR 0004 and its README row to Scope In, a Design "ADR 0004" section, and the narrowed CLAUDE.md sentence.
- round 1 [blocking] Success criterion 3 has no pass condition: now (a) week and `decided_hidden`, (b) rows equal an independent computation in order, (c) fields equal `latest.json`, plus the before/after ids-and-versions no-write check.
- round 1 [minor] One batch in /batch finish can exceed 50 writes: now one `ArtifactData batch` per 50 writes.
- round 2 [minor] Success criterion 3 hard-codes the week: now the week equal to `latest` in `data/index.json`.

## Plan questions

- In the fetch step, does the pending flush run after the keys (step 2) and decisions (step 4) are fetched, followed by a re-list of `decisions` before any show or record flow? (Design, Fetch step; Pending fallback)
- Is `--keys` optional for `pending-add` only (empty `url_norm`, `match_key`, `doc_id` when absent), and required by every other command? (Design, `tools/shortlist.py`; Pending fallback)
- With `find --company` and no `--title`, is the match only a `norm_company` substring match? (Design, `tools/shortlist.py`, `find`)
- In fallback, do pending lines use the URL Aly gave (or the `posting.md` URL), the company and title, and `week_seen: ""`, accepting a possible `match_key` mismatch; and does Show just say the shortlist is unavailable? (Pending fallback; Skill flows)
- For Undo, does `decisions` get a `--url` filter (matching `doc_id` or `url_norm`), so a page-written decision is found by URL or by match_key? (Skill flows, Undo)
- Does the `/batch` finish hook run "Record applied" steps 1-2 for each posting (find, `get`, `doc --existing`) before building the batch, so existing documents carry `if_version`? (Hooks)
- How is the fixture kept byte-identical on Windows: a `.gitattributes` rule (`tests/fixtures/* -text`) or a sha256 check in a test? (Scope In)

## Open

- none
