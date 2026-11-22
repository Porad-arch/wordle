"""Statistics across games: counts and win percentage (R7), streaks and the
saved stats file (R8).

The rules are pure functions on an immutable Stats record. The only file
input and output is in load_stats and save_stats, which take the path as an
argument so tests can point them at a temporary directory.
"""

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

FILE_VERSION = 1
FIELDS = ("played", "won", "current_streak", "longest_streak")


@dataclass(frozen=True)
class Stats:
    played: int = 0
    won: int = 0
    current_streak: int = 0
    longest_streak: int = 0

    @property
    def lost(self):
        # Worked out, never stored, so it can't disagree with played and won.
        return self.played - self.won


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
        )
    return Stats(
        played=stats.played + 1,
        won=stats.won,
        current_streak=0,
        longest_streak=stats.longest_streak,
    )


def win_percentage(stats):
    """Whole-number percentage of games won, halves rounded up; 0 if none."""
    if stats.played == 0:
        return 0
    # Integer form of floor(100 * won / played + 0.5), with no float error.
    return (200 * stats.won + stats.played) // (2 * stats.played)


def default_stats_path():
    """Where the stats live: the home directory, outside this public repo."""
    return Path.home() / ".wordle_stats.json"


def _is_count(value):
    # bool is a subclass of int in Python, so rule it out explicitly.
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _from_dict(data):
    """Build Stats from file data, or return None if it is not believable."""
    if not isinstance(data, dict) or data.get("version") != FILE_VERSION:
        return None
    values = [data.get(name) for name in FIELDS]
    if not all(_is_count(v) for v in values):
        return None
    stats = Stats(*values)
    if not (stats.current_streak <= stats.longest_streak <= stats.won <= stats.played):
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
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
