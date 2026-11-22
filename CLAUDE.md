# wordle

A terminal word-guessing game. Standing rules for every session in this repo.

## Read these first

`problem.md` (the problem and the numbered requirements), `spec.md` (how the code
meets them), `docs/decisions/` (why things are the way they are), and the newest
`handoff-round-<N>.md` if one exists.

## Commands

    python3 main.py        # play
    python3 -m pytest      # run the tests

## How this repo works

- **Requirements come first.** `problem.md` holds numbered requirements R1, R2,
  … Numbers are never reused. A changed requirement keeps its number and says
  what changed; a removed one stays in the file, marked removed.
- **Rules are separate from input and output.** Everything testable lives in
  `game.py`, `words.py`, and `stats.py` as pure functions and plain state
  (`stats.py` also holds the stats-file load and save). `main.py` only
  prints and reads. Do not put a rule in `main.py`.
- **Every requirement is named in a test.** Test names start with the
  requirement ID, for example `test_r3_...`. When a requirement changes, its
  tests change with it in the same round.
- **Tests must actually run.** A skipped test has not passed. Nothing may be
  added that cannot run with `python3 -m pytest` on a plain Python install.
- **No API keys, no logins, no paid services, no network.** The word list is
  compiled into the program on purpose.

## Commits

- Small steps, one change per commit.
- The message says what changed and why. Never `update`, `fix`, or `wip`.
- **Never undo or amend a commit**, and never force-push.
- Push at the end of each working session.

## Never commit

Transcripts (`.jsonl`), API keys or passwords, `.venv`, `__pycache__`,
`node_modules`, or personal information. This repository is public.

## Each round

Requirements into `problem.md` first and pushed before anything else. Then
update `spec.md`, write tests for every new or changed requirement, implement
until all tests pass including the old ones, and add a decision record in
`docs/decisions/` as a Y-statement for a decision that had real alternatives.
