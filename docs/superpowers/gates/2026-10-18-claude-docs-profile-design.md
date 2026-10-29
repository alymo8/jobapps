# Gate: Profile, stories and answers in Claude Docs: design

- **Spec:** docs/superpowers/specs/2026-10-18-claude-docs-profile-design.md
- **Spec SHA-256:** 335f0291d1844f49d7a899ce749206bbb9de2fa177e7f72cd1f008d39d4f63fc
- **Verdict:** pass
- **Date:** 2026-10-18
- **Rounds:** 2 discovery + 0 verification

## Key decisions

- Move profile, stories and answers into Claude Docs and let Claude Code write to the Profile doc only, narrowing ADR 0002 (Purpose, Decisions)
- Stories and Answers stay read-only from Claude Code (Scope Out, Decisions)
- Every profile write goes through `write-source.md`: pull first, one anchored edit, re-pull and verify; never a blind overwrite (Design, write procedure)
- On a `find_none` conflict, retry once from a fresh pull and then stop; never fall back to a local file (Design, write procedure step 5)
- Batch subagents never write the profile; the orchestrator does (Design, Skill and tool changes)
- `/followup` now pulls the sources, including in `--dry-run` (Design, Skill and tool changes)
- `build_cover_letter.py` reads `sources/profile.md` and fails with a JSON error when it is missing (Design, Decisions)
- CI installs PyMuPDF so the build-script tests run (Scope In)
- ADR 0003 supersedes ADR 0002 (Scope In, Design ADR 0003)
- The live write test adds and then deletes a line in the user's real Profile doc (Success criterion 5)
- The main checkout's original root files go to the Recycle Bin after the merge; their `.gitignore` lines stay (Scope In, Decisions)
- Old file names inside the user's doc text stay as they are; a mapping sentence in `pull-sources.md` covers them (Scope Out, Design)

## Findings fixed

- round 1 [blocking] Success criterion 3 contradicts the old-name mapping: criterion 3 excludes the mapping line by its words, and the sentence must be one line.
- round 1 [blocking] New tests cannot run in CI as written: `ci.yml` installs PyMuPDF (Scope In).
- round 1 [blocking] `/followup --dry-run` versus the new pull step: dry runs pull; the bullet says what they write.
- round 1 [blocking] ADR 0002 is narrowed but not marked: 0002 becomes `superseded` by 0003; the Design summarises 0003.
- round 1 [blocking] Line counts were listed in the wrong order: fixed.
- round 1 [minor] Stale "local-only" wording in workday.md: dropped where it describes the profile.
- round 1 [minor] Spec index row not updated: the README rows are in Scope.
- round 1 [minor] pull-sources.md intro goes stale: its intro and "When it runs" are in Scope.
- round 2 [minor] `/followup --dry-run` wording after the rename: the clause now says "no Profile doc writes".
- round 2 [minor] Other `pull-sources.md` lines that name the skills: the opening skill list and the Failure wording are in Scope.
- round 2 [plan, settled in the spec] When the root files go to the Recycle Bin: after the merge, `.gitignore` lines kept.

## Plan questions

- What anchor applies when a section's last line is not unique, or the section is only a heading (the heading line, a multi-line `find`, or the `nth` option)? (Design, write procedure step 2)
- Which tool computes and checks the step 4 "exactly the intended lines" difference? (Design, write procedure step 4)
- When one reply carries several reusable answers, is it one procedure run per answer, in sequence, one "Saved to profile" line each? (Design, write procedure)
- What exact `update` call shape goes into `write-source.md` (copied from the call verified on the throwaway doc)? (Design, write procedure step 3)
- Is the missing-profile check made before `compile_tex` and before the `.tex` is written, and does the error report keep `md`, `words`, `greeting_ok`, `signoff_ok` beside `ok` and `error`? (Design, `tools/build_cover_letter.py`; Tests)

## Open

- none
