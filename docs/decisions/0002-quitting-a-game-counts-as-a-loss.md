# 0002. A game quit partway through counts as a loss

- Status: accepted
- Round: 2
- Requirements: R7, R8

## Decision

In the context of **counting games and winning streaks (R7, R8)**,

facing **a player who stops a game before it ends, with Ctrl-C or end of
input, possibly before making any guess**,

we decided for **recording every started game that isn't won as a loss:
played goes up by one, lost goes up by one, and the current streak goes back
to 0**,

and neglected **leaving abandoned games out of the statistics, and counting
them only if at least one guess had been made**,

to achieve **streaks and win percentages that mean something, because a
player can't protect a streak by quitting a game that is going badly**,

accepting **that a player who quits by accident, or opens the game and
leaves straight away, loses their streak**.

## Notes

- The rule lives in `stats.record_game`: a game counts as a win only if
  `game.is_won`. `main.py` doesn't decide anything. It just hands over the
  unfinished game.
- Saying "n" at the "Play again?" prompt isn't quitting a game. No game has
  started yet, so nothing is recorded.
- Chosen by the project owner at the start of round 2.
