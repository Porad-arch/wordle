# wordle

A word-guessing game for the terminal. A hidden five-letter word, six tries,
and after each guess every letter tells you whether it is in the right place,
in the word somewhere else, or not in the word at all.

It runs offline with no account, no ads, and no limit on how many games you
play. The word list is built into the program.

## Play

    python3 main.py

Add `--no-color` if your terminal does not show the coloured squares:

    python3 main.py --no-color

After each guess, the symbols under the letters mean:

| Symbol | Meaning |
|---|---|
| `+` | right letter, right place |
| `?` | the letter is in the word, but somewhere else |
| `.` | the letter is not in the word |

## Run the tests

    python3 -m pytest

Requires Python 3 and `pytest` (`python3 -m pip install pytest`). Nothing else.

## How it is laid out

- `game.py` — the rules: scoring, attempts, win and loss. No input or output.
- `words.py` — the built-in word list and the random pick.
- `main.py` — the terminal front end.
- `tests/` — one test file per module; each test is named for the requirement
  it checks.
- `problem.md` — who this is for and the numbered requirements.
- `spec.md` — how the code meets them.
