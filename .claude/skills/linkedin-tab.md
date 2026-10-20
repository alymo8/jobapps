# One light LinkedIn tab

A shared procedure file, not a skill: `/outreach`, `/followup` and `/batch`'s LinkedIn subagents
follow it whenever they use LinkedIn. A LinkedIn tab takes several hundred MB and grows with every
page opened inside it; several of them at once crashed the user's 16 GB laptop
([ADR 0007](../../knowledge/decisions/0007-light-linkedin-runs.md)).

- **One LinkedIn tab per run.** Create it when the first LinkedIn page is needed (after loading
  `claude-in-chrome`) and use only its id. Never open a second LinkedIn tab, never touch other tabs.
- **Never leave a message waiting in a tab.** A message is sent or it is not typed; nothing is
  left unsent for the user.
- **Open pages by direct URL**, never by clicking through the feed, and never open
  `https://www.linkedin.com/feed/`:
  - profile: the profile URL from `outreach.md`;
  - people search: `https://www.linkedin.com/search/results/people/?keywords=<words>` (add
    `&network=%5B%22F%22%5D` for 1st-degree connections), then the Current company filter;
  - messaging: `https://www.linkedin.com/messaging/`; sent invitations:
    `https://www.linkedin.com/mynetwork/invitation-manager/sent/`.
- **Recycle the tab every 8 page opens** (a navigation or a search counts; scrolling and typing do
  not): close it (`tabs_close_mcp`) and create a fresh one, then continue. Recycle at once too if a
  page stops responding or a tool call times out. Wait 3–5 seconds after each page open as before.
- **Read as text.** Use `get_page_text` and `find`; take a screenshot only when a click needs a
  position, never as a way to read a page.
- **Close the tab at the end of the run**, including a run that ends early. Exception: on a CAPTCHA,
  rate limit or "restricted activity" warning, leave it open for the user and say which tab it is.
