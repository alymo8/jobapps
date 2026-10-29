# Write to a source doc (the Profile)

A shared procedure file, not a skill: the only way Claude Code changes a Claude Doc. Skills
follow it whenever they save something to `sources/profile.md`: a reusable answer, an `ASK`
replaced by the user's answer, `## Workday work history`, `## Targeting`. Only entries with
`"writable": true` in `config.local.json` `sources` (today the profile) are ever written. Batch subagents never
run it; the orchestrator does.

One run per change. A reply with several reusable answers is several runs, in sequence, each
reporting its own "Saved to profile" line. When runs follow each other with nothing else in
between, the previous run's step 4 pull serves as the next run's step 1 pull. Never delete a line the user wrote, except the one line a
replace targets.

## Steps

If `config.local.json` does not exist, stop and tell the user:
`config.local.json is missing: this repo is not set up yet (README "Setup").`

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
   New answers keep the profile's form: `- <question>: <answer> (the user, YYYY-MM-DD)`, with today's date.
3. **Edit the doc** with Docs `update` (the Claude Docs MCP server's `mcp__<id>__update`, always
   loaded): `ref {"object":"node","id":<node_id>}`, `engine "prose"`,
   `container {"kind":"project","id":<doc id>}`, and
   `payload {"ops":[{"op":"replace","target":{"kind":"find","text":"<old text>"},"with":{"from":{"kind":"inline","content":"<new text>"},"as":"text"}}]}`.
   Both texts are whole lines, each ending in a newline (written `\n` inside the JSON string, a real
   line break in the doc). `<new text>` is always `<old text>` with exactly the intended change and
   nothing else: for an insert, the old text plus the new lines; for a replace, any extended context
   lines unchanged, then the replacement line.
4. **Verify.** Pull the profile again, then
   `git diff --no-index -U0 <scratchpad>/profile.before.md sources/profile.md`. It exits 1 when the
   files differ (expected). Ignoring the `---`/`+++` header lines and the `@@` hunk lines, the
   `+`/`-` lines must be exactly the intended added and removed lines, nothing else. Report one line,
   for example `Saved to profile: "Relocation assistance needed: No".`

## Failure

- The `update` is refused with `find_none` (the doc changed since step 1, for example the user was
  editing it): go back to step 1 once. On a second refusal, stop and tell the user.
- The step 4 difference is not exactly the intended lines: stop and tell the user what changed, quoting
  the difference. Don't try to repair it.
- Any other refusal, or a tool that can't be reached: stop and tell the user. Never write the answer to a
  local file instead.
