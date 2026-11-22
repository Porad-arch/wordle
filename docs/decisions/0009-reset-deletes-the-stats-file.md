# 0009. A reset deletes the stats file, after a y/N question that defaults to No

- Status: accepted
- Round: 6
- Requirement: R11

## Decision

In the context of **R11, which asks for a `--reset-stats` option that
permanently clears all saved statistics after a confirmation message**,

facing **the questions of what "cleared" means on disk and how the player
confirms, when a mistake can't be undone and there is no backup**,

we decided for **deleting `~/.wordle_stats.json` with `reset_stats(path)`,
which does nothing if the file is already gone, only after the saved stats
are shown and the player answers `y` or `yes` to
`Reset all statistics? This cannot be undone. (y/N)`. Any other answer,
Enter, Ctrl-C, or end of input keeps the stats, and the option exits
without starting a game**,

and neglected **writing a version 2 file of all zeros over the old one,
resetting with only a warning and no question, and going on to play after
the question**,

to achieve **a reset that reuses a rule the program already has (a missing
file loads as all zeros, decision 0001) instead of adding a second way to
say "no games", the same result as the README's old advice to delete the
file by hand, and a question that can't clear anything by accident,
including when the game's input is piped in**,

accepting **that after a reset there is no file until the next game is
played, that a damaged file (read as zeros) is reported as "nothing to
reset" and left for the next game to overwrite, and that a script can't
reset without typing an answer, because there is no flag to skip the
question**.

## Alternatives considered

| Option | Why not |
|---|---|
| Write a version 2 file of zeros | Works, but is a second meaning of "no games" alongside the missing file, and it creates a stats file for someone who has just asked to be rid of it. |
| A warning and no question | R11 says "confirmation". Clearing on a typo in the command line can't be undone. |
| Default to Yes on Enter | The usual rule for something that can't be undone is that the safe answer is the default. |
| Go on to play after the question | Mixes two jobs in one run. A player who said no would then be asked for a level they didn't come for. |

## Notes

- Chosen by the project owner at the start of round 6: the y/N question
  defaulting to No, exit afterwards, show the current stats first (and no
  question when there is nothing to reset), and delete the file.
- This session chose that a missing file is not an error, that only `y` and
  `yes` (any case, spaces trimmed) count, and the exit status (0, or 1 when
  the file can't be deleted).
- The stats file format is unchanged, so no `version` bump was needed.
