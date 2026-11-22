# 0003. Statistics go in a new `stats.py` module

- Status: accepted
- Round: 2
- Requirements: R7, R8

## Decision

In the context of **CLAUDE.md's rule that testable rules live in pure
modules and `main.py` only prints and reads**,

facing **new rules (counts, win percentage, streaks) plus the program's
first file input and output**,

we decided for **a third module, `stats.py`, holding an immutable `Stats`
record and pure functions, with the file reading and writing in two small
functions that take the path as an argument**,

and neglected **adding the statistics to `game.py`, and putting the loading
and saving in `main.py`**,

to achieve **`game.py` staying about one game while `stats.py` is about many,
and the save/load code being tested against a temporary folder, not left
untested in `main.py`**,

accepting **one more module, and a small change to CLAUDE.md so that its list
of rule modules includes `stats.py`**.
