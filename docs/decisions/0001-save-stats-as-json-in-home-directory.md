# 0001. Save statistics as a JSON file in the home directory

- Status: accepted
- Round: 2
- Requirement: R8

## Decision

In the context of **R8, which needs statistics to survive between sessions
with no network, no account, and nothing beyond a plain Python install**,

facing **the need to choose where the numbers live and in what form**,

we decided for **one small JSON file at `~/.wordle_stats.json`, written by
renaming a temporary file over it, and read back as all zeros if it is
missing or damaged**,

and neglected **a file in the project folder, a SQLite database, Python's
`shelve`/`pickle`, and a plain `key=value` text file**,

to achieve **statistics that follow the player whichever folder they run the
game from, can never be committed to this public repository by accident, and
can be read or deleted by hand**,

accepting **that the file can't be seen from the repo, that two copies of the
game running at the same moment can overwrite each other's last game, and
that a damaged file quietly resets the stats to zero**.

## Alternatives considered

| Option | Why not |
|---|---|
| `stats.json` in the project folder | Lives inside a public repo, so it relies on `.gitignore` to stay out of commits; each clone keeps separate stats. |
| SQLite (`sqlite3`) | Built in, but far more than four numbers need, and the file can't be read without a tool. |
| `pickle` / `shelve` | Not readable by a person, and loading a pickle runs code from the file. |
| `key=value` text | Works, but means writing a parser; JSON is already in the standard library. |

## Notes

- The file carries `"version": 1` so a later round can change the format and
  still recognise old files.
- `lost` isn't stored. It is `played - won`, so the two can't disagree.
- The home-directory location was confirmed by the project owner at the start
  of round 2.
