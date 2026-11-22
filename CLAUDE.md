# wordle

A terminal word-guessing game. Standing rules for every session in this repo.

## Read these first

`problem.md` (the problem and the numbered requirements), `spec.md` (how the code
meets them), `docs/decisions/` (why things are the way they are), and the newest
`handoff-round-<N>.md` if one exists.

## Commands

    python3 main.py        # play
    python3 -m pytest      # run the tests

To try it by hand, always with a scratch `HOME` (see below), and optionally
with a known answer. The stand-in must accept `pick_word`'s `difficulty`
keyword:

    HOME=$(mktemp -d) python3 main.py
    HOME=$(mktemp -d) python3 -c "import main; main.pick_word=lambda difficulty=None: 'CRANE'; main.main([])"

## How this repo works

- **Requirements come first.** `problem.md` holds numbered requirements R1, R2,
  … Numbers are never reused. A changed requirement keeps its number and says
  what changed; a removed one stays in the file, marked removed.
- **Rules are separate from input and output.** Everything testable lives in
  `game.py`, `words.py`, and `stats.py` as pure functions and plain state
  (`stats.py` also holds the stats-file load and save). `main.py` only
  prints and reads. Do not put a rule in `main.py`. That includes how a
  typed answer is understood: `main.py` asks, a rule module parses (for
  example `game.parse_difficulty`).
- **Imports go one way:** `words.py` and `stats.py` may import from
  `game.py`, never the reverse.
- **Every requirement is named in a test.** Test names start with the
  requirement ID, for example `test_r3_...`. When a requirement changes, its
  tests change with it in the same round.
- **Tests must actually run.** A skipped test has not passed. Nothing may be
  added that cannot run with `python3 -m pytest` on a plain Python install.
- **No API keys, no logins, no paid services, no network.** The word list is
  compiled into the program on purpose.
- **Never touch the player's real stats file** (`~/.wordle_stats.json`).
  Tests pass a `tmp_path` to `load_stats` / `save_stats`. To try the game by
  hand, run it as `HOME=$(mktemp -d) python3 main.py`.
- **Existing stats files must keep loading.** A file the loader doesn't
  recognise is read as all zeros, so a careless format change wipes every
  player's stats without a word. When the format changes, bump `version`,
  keep reading the old versions, and add a test that an old file still loads.

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

- Decision records are numbered `0001`, `0002`, … in one sequence across all
  rounds, and are never renumbered. Continue from the highest number there.
- Tests may be committed before the code they check, but that commit won't
  pass on its own. Name every such commit in the handoff so a bisect can
  skip it.
- Write `handoff-round-<N>.md` only when asked, and don't commit it (or a
  CLAUDE.md change made with it) until the owner has read it.
