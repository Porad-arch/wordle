# 0010. The reset option is tested by running `main.main` with fed-in answers

- Status: accepted
- Round: 6
- Requirement: R11

## Decision

In the context of **CLAUDE.md's rule that every requirement is named in a
test, and the earlier rounds' practice of leaving `main.py` untested
because it only prints and reads**,

facing **R11, whose requirement is a command-line option and a question,
both of which only exist in `main.py`, so testing `reset_stats` and
`confirms_reset` alone can't show that `--reset-stats` deletes anything,
asks first, or keeps the game from starting**,

we decided for **a new `tests/test_main.py` that calls
`main.main(["--reset-stats"])` with `input` replaced by a list of answers
(end of input once they run out) and `main.default_stats_path` pointed at
a `tmp_path`, covering R11 only**,

and neglected **moving the reading of the command line into a rule module
(for example a `parse_args(argv)` in `game.py`) and testing only that, and
running `main.py` as a subprocess with a scratch `HOME`**,

to achieve **tests of the whole option as the player uses it (the question
comes first, a no or no answer keeps the file, the game doesn't start)
that run in plain `pytest` with no network and never touch the player's
real stats file**,

accepting **that these tests check some wording on screen (the question,
"No saved statistics to reset.", the first stats line), so changing that
wording means changing a test, and that the rest of `main.py` is still
only checked by hand**.

## Alternatives considered

| Option | Why not |
|---|---|
| `parse_args(argv)` in a rule module | Would test that the flag is recognised, but not that the question is asked before the file goes, which is the part of R11 that matters most. |
| Subprocess with a scratch `HOME` | Closest to the real program, but slower, and it depends on how `python3` is found and on `HOME` being honoured on every platform. |

## Notes

- This session's choice, not the owner's.
- The rules themselves (`confirms_reset`, `reset_stats`) are still in
  `stats.py` and tested there, so `main.py` holds no rule.
