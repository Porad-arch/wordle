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
