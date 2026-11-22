# 0008. Wins from old stats files are "untracked", worked out rather than stored

- Status: accepted
- Round: 5
- Requirement: R10

## Decision

In the context of **R10, which adds a count of wins in 1 to 8 guesses to
statistics that players have been saving since round 2 as version 1 files
with no guess counts**,

facing **the owner's choice that an old file keeps its numbers, starts its
distribution at zero, and the display says how many earlier wins the
distribution doesn't cover, plus the question of how the file and the code
should hold that number**,

we decided for **stats file version 2 with one new field,
`wins_by_guesses`, a list of exactly 8 counts, and working out the earlier
wins as `untracked_wins = won - sum(wins_by_guesses)` instead of storing
them. A version 1 file loads with all its numbers and an empty
distribution, and a version 2 file whose rows add up to more than `won` is
treated as damaged**,

and neglected **storing a separate `untracked_wins` (or `old_wins`) field in
the file, keeping the distribution as a dictionary keyed by guess count
(`{"3": 5, ...}`), and resetting the statistics of anyone with a version 1
file**,

to achieve **one fact stored once, the same way `lost` is worked out from
`played - won` (decision 0001), so the rows, the wins, and the note can
never disagree. No player loses their stats, and a fixed-length list is
simple to check when loading**,

accepting **that the code can't tell a version 1 player's old wins apart
from a damaged version 2 file with too few rows counted (both just show as
untracked wins), that the average leaves the old wins out, and that the list
format ties the file to 8 rows: a level with more than 8 guesses would need
version 3**.

## Alternatives considered

| Option | Why not |
|---|---|
| A stored `untracked_wins` field | Two numbers that must agree with `won`. A hand-edited or damaged file could say 9 wins, 5 in the rows, and 1 untracked. |
| A dictionary `{"1": 0, "2": 1, ...}` | JSON keys are strings, so loading has to turn them back into numbers and check for missing, extra, or out-of-range keys. An 8-item list only needs a length check. |
| Reset stats on a version 1 file | The owner ruled it out, and CLAUDE.md forbids wiping players' stats with a format change. |

## Notes

- The owner chose at the start of round 5: zeros plus a note for old files,
  one distribution for every level (as in 0006), an average line, and text
  bars. How to store and work out the untracked wins was this session's
  choice.
- `GUESS_ROWS = 8` in `stats.py`. A test checks that every level's number of
  guesses fits, so making Easy longer than 8 guesses fails a test instead of
  crashing a game.
