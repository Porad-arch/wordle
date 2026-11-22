# Handoff after round 6

For the session that does round 7. Read `CLAUDE.md` first for the standing
rules. This file covers only what is true now and what came out of round 6.

## Current state

- Branch `main`, pushed to `origin/main`. The last round 6 commit is
  `17453f0`. The working tree is clean apart from this file (and any
  `CLAUDE.md` change made with it), which the owner has not yet reviewed.
- `problem.md` has R1–R6 (round 1), R7–R8 (round 2), round 3's changed R2
  and new R9, round 4's changed R9, round 5's R10, and round 6's R11.
  **There are no round 7 requirements yet.** They have to come from the
  project owner and go into `problem.md`, committed and pushed, before any
  other round 7 work.
- `python3 -m pytest` gives **219 passed**, with nothing skipped:

  | File | Tests | Requirements |
  |---|---|---|
  | `tests/test_game.py` | 47 | R1, R2, R3, R5, R6 (unchanged in round 6) |
  | `tests/test_words.py` | 55 | R4, R9 (unchanged in round 6) |
  | `tests/test_stats.py` | 105 | R7, R8 (37), R10 (44), R11 (24, new) |
  | `tests/test_main.py` | 12 | R11 (new file) |

- Round 6 is done. R11 is implemented, tested, described in `spec.md`
  under "Round 6", and explained in the README. It was tried by hand with
  a scratch `HOME`: answering no, yes, and Enter, with nothing saved, and
  with a version 1 file.

### Round 6 commits

| Commit | What |
|---|---|
| `57e49f4` | Round 6 requirement in `problem.md` (committed before the session started) |
| `d7d07f1` | `spec.md` Round 6 section |
| `9bde675` | R11 tests, written before the code. **Does not pass on its own** (import error in `tests/test_stats.py`; most of `tests/test_main.py` fails too) |
| `d934b1b` | `stats.py`: `reset_stats`, `confirms_reset` |
| `073016c` | `main.py`: `--reset-stats` and `ask_reset` |
| `42c888f` | README |
| `b693ffb` | Decision record 0009 |
| `17453f0` | Decision record 0010 |

### Files

| File | What changed in round 6 |
|---|---|
| `stats.py` | New `confirms_reset(text)`: `True` only for `y`/`yes`, any case, spaces trimmed. New `reset_stats(path)`: deletes the file, does nothing if it is missing, raises `OSError` otherwise. Docstring updated. |
| `main.py` | New `ask_reset(path)`. `main` checks for `--reset-stats` right after working out the path and returns `ask_reset(path)`, so it never loads stats for play or asks for a level. Docstring now says `--reset-stats` is tested. |
| `tests/test_stats.py` | 24 new `test_r11_…` tests (counting each parametrized case). No existing test changed. |
| `tests/test_main.py` | New. 12 `test_r11_…` tests that run `main.main` with fed-in answers. |
| `docs/decisions/0009`, `0010` | New. No older record was changed. |
| `spec.md`, `README.md` | Round 6 described. The README's "delete that file to start again" now points to `--reset-stats`. |
| `game.py`, `words.py` | Unchanged. |
| Stats file | Unchanged. Still version 2. |

## How to run it

    python3 main.py                # play: pick a level, then guess
    python3 main.py --no-color     # without ANSI colours
    python3 main.py --reset-stats  # show the stats, ask y/N, delete on yes, exit
    python3 -m pytest              # all tests

Requires Python 3 and `pytest`, nothing else. Always try it by hand with a
scratch `HOME` (see `CLAUDE.md`). To check the reset by hand, play one game
and then reset, in the same scratch `HOME`:

    H=$(mktemp -d)
    printf 'e\nSTONE\nCRANE\nn\n' | HOME=$H python3 -c "import main; main.pick_word=lambda difficulty=None: 'CRANE'; main.main(['--no-color'])"
    printf 'y\n' | HOME=$H python3 main.py --reset-stats
    ls -A $H        # the stats file is gone (plain ls hides dotfiles)

## What the player sees

    $ python3 main.py --reset-stats
    Played 21   Won 19   Lost 2   Win 90%
    ... (the usual stats block, including the distribution)

    Reset all statistics? This cannot be undone. (y/N):

Nothing is printed after the answer. With no saved games it prints
`No saved statistics to reset.` and doesn't ask. Exit status is 0, or 1
with `(Could not delete <path>: <error>)` if the file can't be deleted.

## Decisions made in round 6, and why

**Chosen by the project owner** (asked before any code was written):

1. **The player answers a y/N question that defaults to No.** A notice
   with no question was ruled out, and so was printing a line after a
   successful reset.
2. **The option exits after the question.** It doesn't go on to play.
3. **The current stats are shown above the question**, so the player sees
   what they would lose. With nothing saved there is no question.
4. **A reset deletes the file.** The other choice was writing a version 2
   file of zeros. A missing file already loads as zeros (0001). See
   `docs/decisions/0009`.

**Made during the round (not asked for, reported to the owner):**

5. **The rules live in `stats.py`** (`confirms_reset`, `reset_stats`), so
   `main.py` holds no rule.
6. **Only `y` or `yes` counts as yes**, in any case with spaces trimmed.
   `yep`, `ye`, and an empty answer are no.
7. **Ctrl-C or end of input at the question is a no.** This also means
   piped input that runs out can't reset anything.
8. **A missing file is not an error** for `reset_stats`, so resetting twice
   is fine.
9. **Exit status 1 only when the file can't be deleted**, with a message
   naming the file. Otherwise 0.
10. **"Nothing to reset" means `played == 0`.** The loader's checks make that
    mean every number is 0. A damaged file loads as zeros, so it is
    reported as nothing to reset and is **not** deleted. The next game
    overwrites it.
11. **`--reset-stats` is checked first** and works alongside `--no-color`.
    Unknown options are still ignored, as before.
12. **The wording:** `Reset all statistics? This cannot be undone. (y/N): `
    and `No saved statistics to reset.`
13. **`main.py` has tests for the first time**, in `tests/test_main.py`, for
    R11 only. They replace `builtins.input` with a list of answers and
    `main.default_stats_path` with a `tmp_path`. A test of the rule modules
    alone couldn't show that the question comes before the delete. See
    `docs/decisions/0010`.
14. **Listed as out of scope in `spec.md`:** a flag to skip the question
    (such as `--yes`), resetting only part of the stats, and keeping a
    backup of the deleted file.
15. **No stats file version bump**, because the format didn't change.

### How the tests were checked against the old code

- `tests/test_main.py` was run test by test against the round 5
  `main.py`. 11 of 12 fail. The one that passes,
  `test_r11_without_the_option_the_stats_are_not_reset`, is a guard on
  purpose and says so in a comment.
- The two tests for Ctrl-C and end of input first passed against the old
  code, because the old code never deletes anything. They were tightened
  before committing, so they now also check that the reset question was the
  one asked.
- `tests/test_stats.py` was run in a scratch copy of the round 5 code with
  do-nothing stand-ins for the two new names (one run with
  `confirms_reset` always yes, one with it always no). Each yes and no case
  fails under the opposite stand-in, and every deletion test fails against
  a reset that does nothing. Two tests pass against a do-nothing reset on
  purpose: `test_r11_resetting_with_no_file_is_not_an_error` and
  `test_r11_reset_leaves_other_files_alone`. They catch a reset that
  crashes or deletes too much.

## Unresolved / candidates for later rounds

- **A reset can't be undone and keeps no backup.** That is what R11 says
  ("permanently cleared"), but a player who types `y` by mistake loses
  everything.
- **No way to reset without typing.** There is no `--yes`, so a script
  can't reset. Deleting the file by hand still works.
- **A damaged stats file says "nothing to reset" and stays on disk.** The
  player sees zeros either way, but the file isn't removed until the next
  game overwrites it. Still no warning when a damaged file is read as
  zeros (from round 2).
- **`ask_play_again` still parses its answer in `main.py`**
  (`answer.strip().lower() in ("y", "yes")`), from round 2. That breaks the
  CLAUDE.md rule that a rule module parses typed answers. It is the same
  rule as `stats.confirms_reset`, but that function is named for the
  reset. A later round could add a general yes/no parser in `game.py` and
  use it for both. This wasn't changed in round 6 because R11 didn't ask
  for it.
- **The command line is read in `main.py`** with `"--no-color" in argv` and
  `"--reset-stats" in argv`. Unknown options and typos (`--reset-stat`) are
  silently ignored, and the game just starts. If more options come, a parser
  in a rule module (or `argparse`) would be worth it, and that needs a
  decision.
- From earlier rounds, still not done:
  - the owner reviewing the commonness ratings in `words.py`
  - the alphabetical tie-break pushing VOICE, WATCH, WATER, and WORDS to
    Normal (decision 0005)
  - the distribution mixing levels
  - stats for each level
  - setting the level from the command line
  - checking that a guess is a real word
  - more than one player
  - two copies of the game overwriting each other's save
  - the same word coming up twice in a row

## Warnings for the next session

- **`tests/test_main.py` drives the real `main.main`.** Every test there
  must use the `stats_path` fixture (or set `main.default_stats_path`
  itself) and replace `input`. Otherwise it reads or deletes the player's
  real `~/.wordle_stats.json`, or hangs waiting for typing. The `answers`
  fixture also replaces `main.pick_word`, so a test that accidentally
  starts a game gets `CRANE` and can't hang on a random word.
- **These tests check wording on screen:** the question (`Reset all
  statistics?`, `cannot be undone`, `(y/N)`), `No saved statistics to
  reset.`, `Played 5   Won 4   Lost 1`, `Guesses to win`, `Difficulty?`,
  and `Guess`. Changing `show_stats`, the level prompt, or the guess prompt
  can break an R11 test.
- **`test_r11_a_reset_that_fails_says_so_and_exits_with_1` replaces
  `main.reset_stats`.** If `main.py` stops importing `reset_stats` by name
  (for example `import stats` and `stats.reset_stats`), the stand-in no
  longer takes effect and the test fails.
- **`--reset-stats` returns before `load_stats` is called for play.**
  Anything added to the start of `main` after that check won't run during a
  reset.
- **Bisect:** the commits that don't pass on their own are `65b839a`
  (round 2), `03bac62` and `d172966` (round 3), `5cee6e5` (round 5), and
  now `9bde675` (round 6). Don't try to fix them.
- **Warnings from earlier rounds still hold:**
  - The stats file is version 2. The next format change must bump to 3,
    keep reading 1 and 2, and add a test for each. `_from_dict` checks
    `in (1, 2)`.
  - `Stats` has five fields. `record_game` must pass `wins_by_guesses` on
    in both branches.
  - `record_game` assumes a win took 1–8 guesses (`GUESS_ROWS`).
  - `average_guesses_to_win` returns a float rounded to tenths, or `None`.
  - `difficulty_score` returns a `(rating, bonus)` tuple, not an int.
  - `words.py` and `stats.py` may import from `game.py`, never the reverse.
  - `Difficulty`'s values are the guess counts (8, 6, 4). `words_for`
    assumes exactly three levels. Don't reorder `pick_word`'s parameters.
  - Apart from R11, `main.py` has no tests. Play it by hand with a scratch
    `HOME`.
- **Decision records go up to 0010.** The next one is `0011`.
