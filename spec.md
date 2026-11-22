# Spec

How the program meets the requirements in `problem.md`. Updated each round.

## Round 1

### Shape of the code

| File | Holds | Tested |
|---|---|---|
| `game.py` | All rules: scoring, attempt counting, win/loss, end-of-game message | Yes |
| `words.py` | The built-in word list and the random pick | Yes |
| `main.py` | Terminal input and output only | No — presentation |
| `tests/` | One test file per module, each test named for a requirement ID | — |

The split is the point: the rules never print and never read input, so each one
can be checked by calling a function and looking at what comes back.

### How each requirement is met

- **R1** — `Game.guess(word)` accepts a guess, upper-cases and trims it, and
  rejects anything that is not exactly five letters (`ValueError`). The answer
  is held in `Game.answer` and never printed while the game runs.
- **R2** — `MAX_ATTEMPTS = 6`. `Game.attempts_left` counts down; a guess after
  the game is over raises `ValueError`.
- **R3** — `score_guess(guess, answer)` returns one `Mark` per letter:
  `CORRECT`, `PRESENT`, or `ABSENT`. It runs in two passes. The first claims
  letters in the right position; the second lets the remaining letters claim
  only what is left over. That ordering is what makes repeated letters behave:
  guessing `EEEEE` against `THESE` scores exactly two letters, not five.
- **R4** — `WORDS` in `words.py` is a 100-word list compiled into the program,
  so there is no file to load and no network call. `pick_word(rng=None)` takes
  an optional seeded generator so tests can fix the answer.
- **R5** — `Game.is_won` / `Game.is_lost` / `Game.is_over`, and
  `result_message(game)` returns the closing line, or `None` while the game is
  still running.
- **R6** — the losing branch of `result_message` contains `game.answer`. The
  winning branch does not use the reveal wording.

### Scoring example

Answer `ABBEY`, guess `BOBBY`:

| Position | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Guess | B | O | B | B | Y |
| Mark | present | absent | correct | absent | correct |

`ABBEY` has two B's. Position 3 lines up and claims one. Position 1 claims the
second. Position 4 has nothing left to claim, so it is absent even though the
answer does contain a B.

### Running it

    python3 main.py
    python3 main.py --no-color
    python3 -m pytest

### Out of scope in round 1

- Checking that a guess is a real word (any five letters are accepted).
- Keeping score across games, saving, or statistics.
- A hard mode, variable word length, or a shared daily word.

## Round 2

### Shape of the code

| File | Holds | Tested |
|---|---|---|
| `stats.py` | The statistics record, how a finished game changes it, and reading and writing the stats file | Yes |
| `main.py` | Now loops: play a game, record it, print the stats, ask to play again | No — presentation |

`stats.py` is a new module rather than more code in `game.py`, because
statistics are about many games and `game.py` is about one. It follows the
same rule: the statistics logic is pure functions on plain values. The only
file input and output in the program is in two small functions,
`load_stats(path)` and `save_stats(stats, path)`, and the tests call them on a
temporary directory.

### How each requirement is met

- **R7** — `Stats` is an immutable record with `played`, `won`,
  `current_streak`, and `longest_streak`. `lost` is worked out as
  `played - won` and is never stored, so the two numbers can't disagree.
  `record_game(stats, game)` returns a new `Stats` with the game added. A game
  counts as won only if `game.is_won` is true. Every other game is a loss,
  **including a game the player quit partway through** (Ctrl-C or end of
  input), so quitting can't be used to protect a streak.
  `win_percentage(stats)` returns a whole number from 0 to 100, rounded to the
  nearest percent with halves rounded up (1 win in 8 games is 13%), and is 0
  when no games have been played. It uses integer arithmetic, so there is no
  floating-point rounding surprise.
- **R8** — a win adds one to `current_streak`. `longest_streak` is the larger
  of itself and the new current streak. A loss sets `current_streak` back to 0
  and leaves `longest_streak` alone. All four numbers, the R7 counts as well
  as the streaks, are saved to `~/.wordle_stats.json` (`default_stats_path()`)
  after every game, so they survive quitting the program. The file is in the
  home directory, outside the repository, so personal statistics can't be
  committed to this public repo by accident.

### The stats file

    {"version": 1, "played": 12, "won": 9, "current_streak": 3, "longest_streak": 5}

- A missing file means no games yet: `load_stats` returns all zeros.
- A file that isn't valid JSON, or whose numbers are impossible (negative,
  not whole numbers, more wins than games, a current streak longer than the
  longest), is also read as all zeros instead of crashing the game. It is
  overwritten at the end of the next game.
- `save_stats` writes to a temporary file next to the real one and renames it
  over the top. A crash during the write leaves the old file whole.
- If the file can't be written (for example, a read-only home directory), the
  game prints a warning and carries on. Losing the save shouldn't stop play.

### Flow of one run

1. Load the stats.
2. Play a game. When it ends, or the player quits partway through, record the
   game, save it, and print the result and the stats.
3. If the player quit partway through, stop. Otherwise ask `Play again? (y/n)`
   and go back to step 2 on `y`.

The stats are shown as:

    Played 12   Won 9   Lost 3   Win 75%
    Current streak 3   Longest streak 5

### Out of scope in round 2

- Resetting the statistics from inside the game (delete the file to reset).
- A breakdown of how many guesses each win took.
- Stats for more than one player on the same computer.
