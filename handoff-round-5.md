# Handoff after round 5

For the session that does round 6. Read `CLAUDE.md` first for the standing
rules. This file covers only what is true now and what came out of round 5.

## Current state

- Branch `main`, pushed to `origin/main`. The last round 5 commit is
  `d2325e5`. The working tree is clean apart from this file (and any
  `CLAUDE.md` change made with it), which the owner has not yet reviewed.
- `problem.md` has R1–R6 (round 1), R7–R8 (round 2), round 3's changed R2
  and new R9, round 4's changed R9, and round 5's new R10. **There are no
  round 6 requirements yet.** They have to come from the project owner and
  go into `problem.md`, committed and pushed, before any other round 6 work.
- `python3 -m pytest` gives **183 passed**, with nothing skipped:

  | File | Tests | Requirements |
  |---|---|---|
  | `tests/test_game.py` | 47 | R1, R2, R3, R5, R6 (unchanged in round 5) |
  | `tests/test_words.py` | 55 | R4, R9 (unchanged in round 5) |
  | `tests/test_stats.py` | 81 | R7, R8 (37), R10 (44, new) |

- Round 5 is done. R10 is implemented, tested, described in `spec.md` under
  "Round 5", and explained in the README. It was played by hand with a
  scratch `HOME`, including one that started from a version 1 stats file.

### Round 5 commits

| Commit | What |
|---|---|
| `bd6c273` | Round 5 requirement in `problem.md` (committed before the session started) |
| `ed61c5b` | `spec.md` Round 5 section |
| `5cee6e5` | R10 tests, written before the code. **Does not pass on its own** (import error in `tests/test_stats.py`) |
| `5430477` | `stats.py`: distribution, untracked wins, average, bar lengths, file version 2 |
| `94209ea` | `main.py` shows the average and the distribution |
| `3c18111` | README |
| `d2325e5` | Decision record 0008 |

### Files

| File | What changed in round 5 |
|---|---|
| `stats.py` | `FILE_VERSION = 2`. New `GUESS_ROWS = 8` and `NO_WINS`. `Stats` has a fifth field, `wins_by_guesses` (a tuple of 8 ints; position 0 is wins in 1 guess). `record_game` adds one to the row for `game.attempts_used` on a win. New `untracked_wins(stats)`, `average_guesses_to_win(stats)`, `bar_lengths(counts, width=20)`. `_from_dict` reads versions 1 and 2. `save_stats` writes `wins_by_guesses` as a list. |
| `main.py` | `show_stats` prints the average line, a blank line, `Guesses to win`, eight rows, and the earlier-wins note when there are any. No rules were added. |
| `tests/test_stats.py` | 44 new `test_r10_…` tests. The R8 test of the file's exact contents now expects version 2 and `wins_by_guesses`. |
| `docs/decisions/0008` | New. No older record was changed. |
| `spec.md`, `README.md` | Round 5 described. |
| `game.py`, `words.py` | Unchanged. |

### The stats file now

    {"version": 2, "played": 21, "won": 19, "current_streak": 7,
     "longest_streak": 9, "wins_by_guesses": [0, 1, 5, 8, 4, 1, 0, 0]}

- Version 1 (no `wins_by_guesses`) still loads with all its numbers and an
  empty distribution, so all its wins are "untracked". It is rewritten as
  version 2 after the next game.
- A version 2 file is read as all zeros if `wins_by_guesses` is missing,
  isn't a list of exactly 8 whole numbers of 0 or more, or adds up to more
  than `won`.
- Any other version is read as all zeros.

## How to run it

    python3 main.py              # play: pick a level, then guess
    python3 main.py --no-color   # without ANSI colours
    python3 -m pytest            # all tests

Requires Python 3 and `pytest`, nothing else. To try it by hand, use the
two commands in the Commands section of `CLAUDE.md`. To check how an old
player's file looks, put a version 1 file in the scratch `HOME` first:

    H=$(mktemp -d)
    printf '{"version": 1, "played": 3, "won": 2, "current_streak": 1, "longest_streak": 2}' > $H/.wordle_stats.json
    printf 'e\nSTONE\nCRANE\nn\n' | HOME=$H python3 -c "import main; main.pick_word=lambda difficulty=None: 'CRANE'; main.main(['--no-color'])"

Piping the answers in like this plays a whole game with no typing.

## Decisions made in round 5, and why

**Chosen by the project owner** (asked before any code was written):

1. **Old files start the distribution at zero, and the display says how
   many earlier wins aren't in it.** Their played, won, and streaks are
   kept. Resetting was ruled out.
2. **One distribution for every level**, as with the other stats
   (decision 0006). Wins in 7 or 8 can only come from Easy.
3. **An average line is shown** as well as the distribution, and the
   existing end-of-game message stays.
4. **The rows are drawn as text bars of `#`**, all eight rows always shown.

**Made during the round (not asked for, reported to the owner):**

5. **Untracked wins are worked out as `won - sum(wins_by_guesses)`, not
   stored**, the same way `lost` is. One fact stored once, so the rows, the
   wins, and the note can't disagree. See `docs/decisions/0008`.
6. **The distribution is an 8-item list in the file**, not a dictionary
   keyed by guess count, so loading only needs a length check (0008).
7. **What counts as a damaged version 2 file** (see above).
8. **The average leaves out untracked wins** (they have no guess count), is
   rounded to one decimal place with halves rounded up using integer
   arithmetic like `win_percentage`, and is `None`, shown as `-`, when
   there are no counted wins.
9. **Bars are one `#` per win until the biggest row passes 20.** Then they
   are scaled so the biggest is 20, halves rounded up, and any row with a
   win keeps at least one `#`. The owner's preview showed bars scaled even
   when they fit.
10. **The row count is fixed at 8** (`GUESS_ROWS`), with a test that every
    level's number of guesses fits.
11. **The wording on screen:** "Average guesses to win", "Guesses to win",
    and "(plus N earlier wins from before guess counts were kept)", with
    "win" for one.
12. **One existing R8 test was changed** (the exact file contents), because
    the file format changed.
13. **Tests were committed before the code** (`5cee6e5`), so that commit
    fails on its own. Against the old code the whole of
    `tests/test_stats.py` fails to import (the new names don't exist). That
    proves the tests can't pass on round 4 code, but it is a blunt check:
    no test was run one by one against the old module with stand-ins for
    the new names.
14. **The README was updated**, including the line describing `stats.py`.
15. **Listed as out of scope in `spec.md`:** a distribution for each level,
    highlighting the row of the game just won, and guessing where untracked
    wins belong.
16. **Decisions 0001 and 0006 were left untouched.** Both mention version 1,
    but neither decision is replaced by the version bump.

## Unresolved / candidates for later rounds

- **Untracked wins never go away.** A player who upgraded from version 1
  will see the "earlier wins" note for ever, and the average and bars will
  never cover those wins. That is what the owner chose, but they may want a
  way to drop the note (for example a reset) later.
- **A damaged version 2 file with too few rows counted looks the same as an
  upgraded player.** Both show as untracked wins, and nothing warns about
  it.
- **The owner still hasn't reviewed the commonness ratings** in `words.py`
  (from round 3; they decide almost everything about levels since round 4).
- **The alphabetical tie-break still pushes some words to a harder level**
  (VOICE, WATCH, WATER, WORDS are everyday words on Normal). Changing this
  means changing decision 0005, which needs the owner.
- **The distribution mixes levels.** A row-3 win on Hard and a row-3 win on
  Easy look the same, and the average favours Hard players, who have
  fewer guesses to use.
- From earlier rounds, still not done: stats for each level, setting the
  level from the command line, checking that a guess is a real word, a
  reset command, more than one player, a warning when a damaged stats file
  is reset, two copies of the game overwriting each other's save, and the
  same word coming up twice in a row.

## Warnings for the next session

- **`Stats` has five fields now.** Code that builds one with positional
  arguments must give `wins_by_guesses` as the fifth, or leave it out to get
  an empty distribution. `record_game` must pass it on in both branches, or
  a loss would wipe it.
- **`record_game` assumes `game.attempts_used` is 1–8 on a win.** A level
  with more than 8 guesses would crash it with an `IndexError`. The test
  `test_r10_every_level_fits_in_the_distribution` fails first, but R10
  names the rows 1–8, so lengthening Easy means a requirement question for
  the owner and a stats file version 3.
- **The stats file is version 2.** The next format change must bump to 3,
  keep reading **both** 1 and 2, and add a test for each old version.
  `_from_dict` checks the version with `in (1, 2)`; don't swap that back to
  `== FILE_VERSION`.
- **`average_guesses_to_win` returns a float rounded to tenths, or `None`.**
  `main.py` formats it with `:.1f`. Compare it in tests to values like
  `2.7`, which works because the result is `tenths / 10`.
- **Bisect:** the commits that don't pass on their own are `65b839a`
  (round 2), `03bac62` and `d172966` (round 3), and now `5cee6e5`
  (round 5). Don't try to fix them.
- **Warnings from earlier rounds still hold:**
  - `difficulty_score` returns a `(rating, bonus)` tuple, not an int.
  - `words.py` and `stats.py` may import from `game.py`, never the reverse.
  - `Difficulty`'s values are the guess counts (8, 6, 4). Two equal counts
    would silently make one level an alias of another.
  - `words_for` assumes exactly three levels.
  - Don't reorder `pick_word`'s parameters.
  - `main.py` has no tests. Play it by hand with a scratch `HOME`.
- **Decision records go up to 0008.** The next one is `0009`.
