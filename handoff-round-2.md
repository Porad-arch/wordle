# Handoff after round 2

For the session that does round 3. Read `CLAUDE.md` first for the standing
rules. This file covers only what is true now and what came out of round 2.

## Current state

- Branch `main`, pushed to `origin/main`. The last round 2 commit is `dc763b6`.
  The working tree was clean when this file was written.
- `problem.md` has R1–R6 (round 1) and R7–R8 (round 2). **There are no
  round 3 requirements yet.** They have to come from the project owner and go
  into `problem.md`, committed and pushed, before any other round 3 work.
- `python3 -m pytest` gives **65 passed**: 28 from round 1 in
  `tests/test_game.py` and `tests/test_words.py`, and 37 from round 2 in
  `tests/test_stats.py`. Nothing is skipped.
- Round 2 is done: R7 (played, won, lost, win percentage) and R8 (current and
  longest streak, saved between sessions) are implemented, tested, and
  described in `spec.md` under "Round 2".

### Files

| File | What it is |
|---|---|
| `game.py` | One game: scoring (R3), attempts (R2), win/loss and the end message (R5, R6). Unchanged in round 2. |
| `words.py` | The 100-word built-in list and `pick_word` (R4). Unchanged in round 2. |
| `stats.py` | **New in round 2.** The immutable `Stats` record, `record_game`, `win_percentage`, `default_stats_path`, `load_stats`, `save_stats`. |
| `main.py` | Terminal input and output only. Round 2 split it into `play_one`, `show_stats`, `ask_play_again`, and a `main` loop. |
| `tests/test_stats.py` | **New in round 2.** Every test is named `test_r7_…` or `test_r8_…`. |
| `docs/decisions/0001–0003` | **New in round 2.** The first decision records in the repo. |

## How to run it

    python3 main.py              # play; stats are shown after each game
    python3 main.py --no-color   # without ANSI colours
    python3 -m pytest            # all tests

Requires Python 3 and `pytest`, nothing else.

**To try the game by hand without touching your real statistics**, point
`HOME` at a scratch folder:

    HOME=$(mktemp -d) python3 main.py

To force a known answer while trying it out (this changes nothing on disk):

    HOME=$(mktemp -d) python3 -c "import main; main.pick_word=lambda: 'CRANE'; main.main([])"

## Decisions made in round 2, and why

Four of these were asked of the project owner before any code was written.
The rest were made during the round and reported to the owner at the end.

**Chosen by the project owner:**

1. **A game quit partway through (Ctrl-C or end of input) counts as a loss**,
   even if no guess was made, and resets the current streak. Otherwise a
   player could protect a streak by quitting a game that was going badly. See
   `docs/decisions/0002`.
2. **The stats file is `~/.wordle_stats.json` in the home directory**, not in
   the project folder. It follows the player to whatever folder they run from,
   and it can never be committed to this public repo by accident. See
   `docs/decisions/0001`.
3. **The win percentage is a whole number**, and 0% when no games have been
   played.
4. **Stats are shown after every game, followed by "Play again? (y/n)"**, so a
   streak can build within one run.

**Made during the round (not asked for, but reported to the owner):**

5. R8's "save these statistics" was read as **save all of them**: the R7
   counts as well as the streaks.
6. **Statistics got their own module, `stats.py`**, instead of going into
   `game.py`: `game.py` is about one game, `stats.py` is about many. CLAUDE.md
   was changed to list it among the rule modules. See `docs/decisions/0003`.
7. **`lost` is worked out as `played - won` and never stored**, so the two
   can't disagree.
8. **The win percentage rounds halves up** (1 win in 8 games shows 13%),
   using integer arithmetic. Python's `round()` would round 12.5 down to 12,
   so don't "simplify" the code to use it.
9. **The file is JSON with a `"version": 1` field.** The full format is in
   `spec.md`.
10. **A missing or damaged file loads as all zeros, with no warning.** Damaged
    means the JSON doesn't parse, the version is wrong, a field is missing, a
    value is not a whole number (`true`, `5.5`, and `"5"` are rejected), or the
    numbers are impossible: the check is
    `current_streak <= longest_streak <= won <= played`. The bad file is
    overwritten after the next game. This keeps a bad file from ever stopping
    the game from starting.
11. **Saving writes a temporary file in the same folder and then renames it
    over the real one** (`os.replace`), so a crash during the write can't
    leave half a file.
12. **If the save fails, `main.py` prints a warning and play carries on.**
13. **Saying "n", pressing Enter, or pressing Ctrl-C at "Play again?" records
    nothing**, because no game has started. Only `y` or `yes` (in any case)
    starts another game.
14. **After a quit, the stats are shown and the program exits** without
    asking to play again.

## Unresolved / out of scope (candidates for later rounds)

From round 1, still not done:

- Checking that a guess is a real word. Any five letters are accepted.
- Hard mode, a different word length, or a shared daily word.

From round 2:

- **No reset command.** The only way to reset is to delete
  `~/.wordle_stats.json`. The README says so.
- **No count of how many guesses each win took.** If a round asks for one, the
  file format has to change (see the warnings below).
- **One set of stats per computer account.** There are no separate players.
- **A damaged stats file is lost without telling the player.** The owner may
  want a warning or a backup copy. That needs a requirement or the owner's
  say-so first.
- **Two copies of the game running at once can overwrite each other's last
  game**, because each one loads at start-up and saves the whole record. This
  was accepted in decision 0001.

## Warnings for the next session

- **Commit `65b839a` does not pass on its own.** It added
  `tests/test_stats.py` before `stats.py` existed (tests first, on purpose).
  Every commit from `c590166` on passes. If you bisect, skip `65b839a`. Don't
  try to "fix" it: commits are never amended.
- **Don't run `main.py` in a way that writes to the real home directory** (see
  "How to run it" above). Tests never touch the real file: they pass
  `tmp_path` to `load_stats`/`save_stats`, and the one test of
  `default_stats_path()` only checks the path it returns.
- **The file format is now something players depend on.** People may already
  have a `~/.wordle_stats.json`. Because of decision 10 above, a format change
  that the loader doesn't recognise will **quietly reset everyone's stats to
  zero**. If round 3 adds a field, either bump `version` and still read
  version 1 files, or accept missing new fields with a default. Add a test
  that a version 1 file still loads.
- **Adding a field to `Stats` means updating `FIELDS` in `stats.py`**,
  `_from_dict`'s checks, and `test_r8_the_file_holds_all_the_statistics`,
  which compares the whole saved dictionary exactly.
- **The quit-counts-as-a-loss rule is in `stats.record_game`**, not in
  `main.py`: anything that isn't `game.is_won` is a loss. If a later round
  adds a way to end a game that shouldn't count (for example a "give up and
  don't record" command), it must be handled there and tested there.
- **`main.py` has no tests**, by the repo's design. Keep any new rule out of
  it. Round 2's flow (when to record, what to show) is only checked by hand.
- **Decision records start at 0001 and the highest is 0003.** The next one is
  `0004`.
