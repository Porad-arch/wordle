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

Under that it shows the average number of guesses your wins took, and how
many games you won in 1, 2, 3, 4, 5, 6, 7, or 8 guesses, as a row of `#`
for each:

    Guesses to win
      1 | 0
      2 | # 1
      3 | ##### 5
      4 | ######## 8
      ...

Wins from before the game kept guess counts (a stats file from an older
version) aren't in the rows or the average. The game says how many there are.

The statistics are saved in `~/.wordle_stats.json` in your home directory, so
they carry over to the next time you play.

To start again from zero:

    python3 main.py --reset-stats

It shows your current statistics and asks
`Reset all statistics? This cannot be undone. (y/N)`. Only `y` or `yes`
clears them. Anything else, or just pressing Enter, keeps them. Either way
it then exits, so run `python3 main.py` to play. A reset deletes the stats
file.

## Run the tests

    python3 -m pytest

Requires Python 3 and `pytest` (`python3 -m pip install pytest`). Nothing else.

## How it is laid out

- `game.py` — the rules: scoring, levels and attempts, win and loss. No input
  or output.
- `words.py` — the built-in word list, each word's difficulty rating, and the
  random pick.
- `stats.py` — games played, won and lost, win percentage, streaks, guesses
  per win, and the saved stats file, including resetting it.
- `main.py` — the terminal front end, and the `--reset-stats` option.
- `tests/` — one test file per module; each test is named for the requirement
  it checks.
- `problem.md` — who this is for and the numbered requirements.
- `spec.md` — how the code meets them.
- `docs/decisions/` — why things are the way they are.
