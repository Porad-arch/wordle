# wordle

A word-guessing game for the terminal. A hidden five-letter word, a limited
number of tries, and after each guess every letter tells you whether it is in the right place,
in the word somewhere else, or not in the word at all.

It runs offline with no account, no ads, and no limit on how many games you
play. The word list is built into the program.

## Play

    python3 main.py

Add `--no-color` if your terminal does not show the coloured squares:

    python3 main.py --no-color

Before each game, pick a level. Press Enter for Normal:

| Level | Tries | Words |
|---|---|---|
| Easy | 8 | the easiest third of the word list |
| Normal | 6 | the middle third |
| Hard | 4 | the hardest third |

How common a word is decides first: a less common word is always on a
harder level than an everyday one. Among words that are equally common, a
word is harder if it contains J, Q, X, or Z, or has a repeated letter.

After each guess, the symbols under the letters mean:

| Symbol | Meaning |
|---|---|
| `+` | right letter, right place |
| `?` | the letter is in the word, but somewhere else |
| `.` | the letter is not in the word |

## Statistics

After every game the game shows how many you have played, won, and lost, your
win percentage, and your current and longest winning streak, then asks
whether to play again. Games on every level count toward the same
statistics. Quitting partway through a game (Ctrl-C) counts as a
loss.

The statistics are saved in `~/.wordle_stats.json` in your home directory, so
they carry over to the next time you play. Delete that file to start again
from zero.

## Run the tests

    python3 -m pytest

Requires Python 3 and `pytest` (`python3 -m pip install pytest`). Nothing else.

## How it is laid out

- `game.py` — the rules: scoring, levels and attempts, win and loss. No input
  or output.
- `words.py` — the built-in word list, each word's difficulty rating, and the
  random pick.
- `stats.py` — games played, won and lost, win percentage, streaks, and the
  saved stats file.
- `main.py` — the terminal front end.
- `tests/` — one test file per module; each test is named for the requirement
  it checks.
- `problem.md` — who this is for and the numbered requirements.
- `spec.md` — how the code meets them.
- `docs/decisions/` — why things are the way they are.
