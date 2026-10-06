# ADR 0001: Workday sign-in via Chrome saved passwords

- **Status:** accepted
- **Date:** 2026-10-05

## Context
Workday postings are the largest group of blocked applications: every Workday tenant has its own
candidate account, and `/apply` stopped at the sign-in wall. the user has accounts at many tenants with
passwords saved in Chrome. A spike on 2026-10-05 (Manulife) showed Chrome autofills the email and
password when the Sign In dialog opens, and clicking Sign In logs in. Claude's browser rules forbid
it to type passwords or create accounts on third-party sites.

## Decision
Claude signs in to Workday only by letting Chrome autofill the saved credentials and clicking
Sign In. It never types into a password field and never fills Create Account. With no usable
saved login, the user signs in or creates the account in the open tab (normal run), or the posting is
dead-lettered as `BLOCKED` with Detail `NO-WORKDAY-LOGIN <tenant> <workday url>: ...` (batch).
Save and Continue between wizard steps (a draft on the user's account) needs no approval; ticking the
terms/consent checkbox and Submit need the user's explicit OK.

## Consequences
Workday postings flow through `/apply` and `/batch` like Greenhouse ones once a tenant has a saved
login. Each new tenant still needs the user once (create the account, let Chrome save the password).
Rejected: the user signs in by hand every time (slow in batches); Claude types a stored password
(credentials in context, disallowed); Claude creates accounts (disallowed).
