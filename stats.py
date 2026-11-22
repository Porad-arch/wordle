"""Statistics across games: counts and win percentage (R7), streaks and the
saved stats file (R8), how many guesses each win took (R10), and resetting
the saved statistics (R11).

The rules are pure functions on an immutable Stats record. The only file
input and output is in load_stats, save_stats, and reset_stats, which take
the path as an argument so tests can point them at a temporary directory.
"""

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

FILE_VERSION = 2
FIELDS = ("played", "won", "current_streak", "longest_streak")

# One row for each number of guesses a win can take: 1 to 8 (R10). Easy,
# the level with the most guesses, has 8.
GUESS_ROWS = 8
NO_WINS = (0,) * GUESS_ROWS


@dataclass(frozen=True)
class Stats:
    played: int = 0
    won: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    # wins_by_guesses[0] is wins in 1 guess, [7] is wins in 8 (R10).
    wins_by_guesses: tuple = NO_WINS

    @property
    def lost(self):
        # Worked out, never stored, so it can't disagree with played and won.
        return self.played - self.won


def _add_win(counts, guesses):
    counts = list(counts)
    counts[guesses - 1] += 1
    return tuple(counts)


def record_game(stats, game):
    """Return new Stats with `game` added.

    Only a won game is a win. Anything else is a loss, including a game the
    player quit before it finished, so quitting can't protect a streak.
    """
    if game.is_won:
        current = stats.current_streak + 1
        return Stats(
            played=stats.played + 1,
            won=stats.won + 1,
            current_streak=current,
            longest_streak=max(stats.longest_streak, current),
            wins_by_guesses=_add_win(stats.wins_by_guesses, game.attempts_used),
        )
    return Stats(
        played=stats.played + 1,
        won=stats.won,
        current_streak=0,
        longest_streak=stats.longest_streak,
        wins_by_guesses=stats.wins_by_guesses,
    )


def win_percentage(stats):
    """Whole-number percentage of games won, halves rounded up; 0 if none."""
    if stats.played == 0:
        return 0
    # Integer form of floor(100 * won / played + 0.5), with no float error.
    return (200 * stats.won + stats.played) // (2 * stats.played)


def untracked_wins(stats):
    """Wins with no guess count: those recorded before round 5 (R10)."""
    return stats.won - sum(stats.wins_by_guesses)


def average_guesses_to_win(stats):
    """Average guesses per win, to one decimal place with halves rounded up.

    Only wins in the distribution count, since untracked wins have no guess
    count. None if there are no such wins.
    """
    wins = sum(stats.wins_by_guesses)
    if wins == 0:
        return None
    guesses = sum(n * count for n, count in enumerate(stats.wins_by_guesses, 1))
    # Integer form of floor(10 * guesses / wins + 0.5), with no float error.
    tenths = (20 * guesses + wins) // (2 * wins)
    return tenths / 10


def bar_lengths(counts, width=20):
    """How many marks to draw for each row of the distribution.

    One mark per win while the biggest row fits in `width`. Beyond that the
    biggest row gets `width`, the rest are scaled to match (halves rounded
    up), and a row with any wins keeps at least one mark.
    """
    biggest = max(counts, default=0)
    if biggest <= width:
        return list(counts)
    return [
        max(1, (2 * c * width + biggest) // (2 * biggest)) if c else 0
        for c in counts
    ]


def default_stats_path():
    """Where the stats live: the home directory, outside this public repo."""
    return Path.home() / ".wordle_stats.json"


def _is_count(value):
    # bool is a subclass of int in Python, so rule it out explicitly.
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _from_dict(data):
    """Build Stats from file data, or return None if it is not believable.

    Version 1 files (before round 5) have no guess counts, so their
    distribution starts empty and all their wins count as untracked.
    """
    if not isinstance(data, dict) or data.get("version") not in (1, 2):
        return None
    values = [data.get(name) for name in FIELDS]
    if not all(_is_count(v) for v in values):
        return None
    if data["version"] == 1:
        counts = NO_WINS
    else:
        counts = data.get("wins_by_guesses")
        if not (
            isinstance(counts, list)
            and len(counts) == GUESS_ROWS
            and all(_is_count(c) for c in counts)
        ):
            return None
        counts = tuple(counts)
    stats = Stats(*values, wins_by_guesses=counts)
    if not (stats.current_streak <= stats.longest_streak <= stats.won <= stats.played):
        return None
    if untracked_wins(stats) < 0:
        return None
    return stats


def load_stats(path):
    """Read stats from `path`. A missing or damaged file means a fresh start."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return Stats()
    return _from_dict(data) or Stats()


def save_stats(stats, path):
    """Write stats to `path`, replacing it in one step.

    The data goes to a temporary file in the same folder first and is then
    renamed over the real one, so a crash mid-write never leaves half a file.
    Raises OSError if the file can't be written.
    """
    path = Path(path)
    data = {"version": FILE_VERSION}
    data.update({name: getattr(stats, name) for name in FIELDS})
    data["wins_by_guesses"] = list(stats.wins_by_guesses)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def confirms_reset(text):
    """True only if the answer to the reset question is yes (R11).

    The question defaults to No, so an empty answer, or anything that isn't
    y or yes, keeps the statistics.
    """
    return text.strip().lower() in ("y", "yes")


def reset_stats(path):
    """Delete the stats file at `path`, so the stats load as all zeros (R11).

    A missing file is already a fresh start, so there being no file is not
    an error. Raises OSError if the file exists but can't be removed.
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
