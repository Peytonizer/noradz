# Noradz

Personal landing page for the noradz domain — collates and showcases Matt's AI
projects. Tech stack not yet decided beyond "web-based"; likely a static site
(similar pattern to Strata / Torn Battlecards) deployed via GitHub Pages, but
confirm before scaffolding rather than assuming.

## STYLE
Auto mode: work autonomously with minimal narration. Don't explain what you're doing or why
by default — just do it. Flag risks, gaps, or better approaches concisely, and still explain
when something is non-obvious, risky, or genuinely worth knowing.

## CLARIFYING QUESTIONS
When intent is ambiguous, ask before proceeding. Ask directly in the terminal as plain
text — this environment doesn't support interactive button/select UI.

## FILE TOOLS vs BASH
File tools (Read/Edit/Write/Grep/Glob) are the single source of truth. Never verify file
contents via bash after editing — trust the tool's confirmation. Use bash only for what
file tools can't do (builds, installs, git, running the site locally, unedited file searches).
If a bash read looks stale or inconsistent, re-read with the Read tool and trust that result.

## EDITS
Make targeted, minimal changes. No full-file rewrites unless explicitly required or the
file is still small/early-stage. Don't repeat back confirmed content — just make the
change and explain it.

## GIT & GITHUB
- After each change that works (page renders, feature does what it's supposed to), commit
  automatically. Write a clear, specific commit message (not "update file").
- Push to `origin` automatically once a change is committed and working — no need to ask
  first. Still show a one-line summary of what's being pushed.
- Never commit secrets: API keys, tokens, analytics IDs meant to stay private, or `.env`
  contents. A `.gitignore` covering `.env` and any local config must exist before the
  first commit.
- If a commit would include something that looks like a secret or personal info beyond
  what's meant to be public on the landing page, stop and flag it instead of committing.

## TOKEN ECONOMY
Flag when a conversation is running long and consuming more tokens than warranted. When
flagging, give a compact handover summary and a ready-to-paste continuation prompt, then stop.

## PROJECT SCAFFOLDING
Ensure README.md and CHANGELOG.md exist; check before creating rather than overwriting.
- README: what the project does, setup steps, how to run/preview it locally.
- CHANGELOG: one line per meaningful change, added at the same time as the related commit.
Skip a formal milestone plan unless the project grows enough to need one.

## DOCUMENTATION
Keep everything well documented as you go, not as an afterthought:
- Every script/config gets a short comment on what it does and why, not just what the
  code already makes obvious.
- README stays current with any change to setup, usage, or config — update it in the same
  commit as the change, not later.
- Non-obvious decisions (why a tool/library was chosen, a workaround, a tradeoff) get a
  line in the CHANGELOG or an inline comment at the time they're made, while the reasoning
  is fresh.

## LANGUAGE
Use Australian English spelling and conventions in documentation, prose comments, commit
messages, and chat responses (e.g. "colour", "organise", "behaviour"). Never in code:
variable/function names, config keys, and anything that mirrors a library's own API keep
their standard (usually US) spelling.
