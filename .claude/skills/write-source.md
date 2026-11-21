# Write to a source doc (the Profile)

A shared procedure file, not a skill: the only way Claude Code changes a source (the profile's Claude
Doc or its local file). Skills
follow it whenever they save something to `sources/profile.md`: a reusable answer, an `ASK`
replaced by the user's answer, `## Targeting`. Only entries with
`"writable": true` in `config.local.json` `sources` (today the profile) are ever written. Batch subagents never
run it; the orchestrator does.

One run per change. A reply with several reusable answers is several runs, in sequence, each
reporting its own "Saved to profile" line. When runs follow each other with nothing else in
between, the previous run's step 4 pull serves as the next run's step 1 pull. Never delete a line the user wrote, except the one line a
replace targets.

## Steps

If `config.local.json` does not exist, stop and tell the user:
`config.local.json is missing: this repo is not set up yet (run /onboard, or see README "Setup").`

Run from the repo root.

1. **Pull fresh.** Pull the profile entry alone (the `.claude/skills/pull-sources.md` steps for that
   entry), so the edit starts from the doc as it is now. Copy the result to
   `<scratchpad>/profile.before.md`.
2. **Choose one edit** against text that occurs exactly once in the pulled file:
   - a new answer: insert after the last non-blank line of its section;
   - an empty section (heading only): insert after the heading line;
   - a new section: insert after the file's last non-blank line, the new text starting with a blank
     line (`
## <Heading>
...`);
   - a changed answer (for example an `ASK` line): replace that line.
   Count how often the anchor line occurs in the pulled file (the docs hold nothing else that could
   match). If more than once, extend the anchor upward one line at a time (a multi-line text ending
   with the anchor line) until it occurs once; if it would have to include the line above the
   section's heading, stop and tell the user. Never use the `nth` option.
   New answers keep the profile's form: `- <question>: <answer> (<first name>, YYYY-MM-DD)`, with today's date; `<first name>` is the
   `Preferred first name` line under `## Contact` in the pulled `sources/profile.md` (trailing
   parenthetical note stripped; if that line is missing or `ASK`, the first word of `Full name`).
3. For a Doc entry (`doc_url`): **Edit the doc** with Docs `update` (the Claude Docs MCP server's `mcp__<id>__update`, always
   loaded): `ref {"object":"node","id":<node_id>}`, `engine "prose"`,
   `container {"kind":"project","id":<doc id>}`, and
   `payload {"ops":[{"op":"replace","target":{"kind":"find","text":"<old text>"},"with":{"from":{"kind":"inline","content":"<new text>"},"as":"text"}}]}`.
   Both texts are whole lines, each ending in a newline (written `\n` inside the JSON string, a real
   line break in the doc). `<new text>` is always `<old text>` with exactly the intended change and
   nothing else: for an insert, the old text plus the new lines; for a replace, any extended context
   lines unchanged, then the replacement line.

   For a local entry (`local_path`): Read `<local_path>`, then run
   `python -I -c "import sys; sys.exit(b'\r' in open(sys.argv[1], 'rb').read())" "<local_path>"`;
   exit 1 means the file has CR line endings: stop and tell the user to save it with LF line
   endings (never convert it). Then Edit `<local_path>` with `old_string` = `<old text>` and
   `new_string` = `<new text>`, the same whole-line texts as the Docs payload, with real line
   breaks; Edit's own uniqueness check stands in for `find_none`.
4. **Verify.** Pull the profile again, then
   `git diff --no-index -U0 <scratchpad>/profile.before.md sources/profile.md`. It exits 1 when the
   files differ (expected). Ignoring the `---`/`+++` header lines and the `@@` hunk lines, the
   `+`/`-` lines must be exactly the intended added and removed lines, nothing else. Report one line,
   for example `Saved to profile: "Relocation assistance needed: No".`

## Failure

- The `update` is refused with `find_none` (the doc changed since step 1, for example the user was
  editing it): go back to step 1 once. On a second refusal, stop and tell the user.
- A local profile with CR line endings: stop (step 3, local).
- A local Edit that finds the old text zero or several times: go back to step 1 once; the second
  time, stop and tell the user. An Edit that notes the file changed on disk since it was read still
  applies: do not retry (a retry would add the change twice); go on to step 4, whose check stops on
  the user's other changes.
- The step 4 difference is not exactly the intended lines: stop and tell the user what changed, quoting
  the difference. Don't try to repair it.
- Any other refusal, or a tool that can't be reached: stop and tell the user. Never write it anywhere but
  the profile entry's own source (its Doc or its `local_path`).
