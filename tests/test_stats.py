"""Tests for game statistics (R7) and saved streaks (R8)."""

import json

import pytest

from game import Game
from stats import (
    Stats,
    default_stats_path,
    load_stats,
    record_game,
    save_stats,
    win_percentage,
)


def won_game():
    game = Game("CRANE")
    game.guess("CRANE")
    return game


def lost_game():
    game = Game("CRANE")
    for _ in range(6):
        game.guess("STONE")
    return game


def quit_game():
    # The player made one guess and then stopped, so the game never finished.
    game = Game("CRANE")
    game.guess("STONE")
    return game


def play(results):
    """Record a run of games given as a string such as 'WWLW'."""
    stats = Stats()
    for r in results:
        stats = record_game(stats, won_game() if r == "W" else lost_game())
    return stats


# R7: Track the total number of games played, games won, and games lost, and
#     calculate the player's win percentage.


def test_r7_a_new_player_has_no_games():
    stats = Stats()
    assert (stats.played, stats.won, stats.lost) == (0, 0, 0)


def test_r7_a_win_counts_as_played_and_won():
    stats = record_game(Stats(), won_game())
    assert (stats.played, stats.won, stats.lost) == (1, 1, 0)


def test_r7_a_loss_counts_as_played_and_lost():
    stats = record_game(Stats(), lost_game())
    assert (stats.played, stats.won, stats.lost) == (1, 0, 1)


def test_r7_counts_add_up_over_several_games():
    stats = play("WLWWL")
    assert (stats.played, stats.won, stats.lost) == (5, 3, 2)


def test_r7_a_game_quit_partway_through_counts_as_a_loss():
    stats = record_game(Stats(), quit_game())
    assert (stats.played, stats.won, stats.lost) == (1, 0, 1)


def test_r7_a_game_quit_before_any_guess_counts_as_a_loss():
    stats = record_game(Stats(), Game("CRANE"))
    assert (stats.played, stats.won, stats.lost) == (1, 0, 1)


def test_r7_recording_a_game_does_not_change_the_old_stats():
    before = Stats()
    record_game(before, won_game())
    assert before == Stats()


def test_r7_win_percentage_is_zero_before_any_games():
    assert win_percentage(Stats()) == 0


@pytest.mark.parametrize(
    "results, expected",
    [
        ("W", 100),
        ("L", 0),
        ("WL", 50),
        ("WWL", 67),  # 66.67 rounds up
        ("WLL", 33),  # 33.33 rounds down
        ("WLLLLLLL", 13),  # 12.5: a half rounds up
    ],
)
def test_r7_win_percentage_is_rounded_to_a_whole_number(results, expected):
    assert win_percentage(play(results)) == expected


# R8: Track the player's current and longest winning streak, and save these
#     statistics locally so they persist between sessions.


def test_r8_a_new_player_has_no_streak():
    stats = Stats()
    assert (stats.current_streak, stats.longest_streak) == (0, 0)


def test_r8_wins_in_a_row_build_the_current_streak():
    stats = play("WWW")
    assert stats.current_streak == 3
    assert stats.longest_streak == 3


def test_r8_a_loss_ends_the_current_streak_but_not_the_longest():
    stats = play("WWWL")
    assert stats.current_streak == 0
    assert stats.longest_streak == 3


def test_r8_quitting_a_game_ends_the_streak():
    stats = record_game(play("WW"), quit_game())
    assert stats.current_streak == 0
    assert stats.longest_streak == 2


def test_r8_a_shorter_new_streak_keeps_the_old_longest():
    stats = play("WWWLWW")
    assert stats.current_streak == 2
    assert stats.longest_streak == 3


def test_r8_a_longer_new_streak_becomes_the_longest():
    stats = play("WWLWWWW")
    assert stats.current_streak == 4
    assert stats.longest_streak == 4


def test_r8_saved_stats_load_back_the_same(tmp_path):
    path = tmp_path / "stats.json"
    stats = play("WWLWWW")
    save_stats(stats, path)
    assert load_stats(path) == stats


def test_r8_stats_persist_across_separate_sessions(tmp_path):
    # Each "session" starts from only what is on disk, as a new run would.
    path = tmp_path / "stats.json"
    save_stats(record_game(load_stats(path), won_game()), path)
    save_stats(record_game(load_stats(path), won_game()), path)
    save_stats(record_game(load_stats(path), lost_game()), path)
    save_stats(record_game(load_stats(path), won_game()), path)
    stats = load_stats(path)
    assert (stats.played, stats.won, stats.lost) == (4, 3, 1)
    assert (stats.current_streak, stats.longest_streak) == (1, 2)


def test_r8_the_file_holds_all_the_statistics(tmp_path):
    path = tmp_path / "stats.json"
    save_stats(play("WWL"), path)
    data = json.loads(path.read_text())
    assert data == {
        "version": 1,
        "played": 3,
        "won": 2,
        "current_streak": 0,
        "longest_streak": 2,
    }


def test_r8_a_missing_file_means_no_games_yet(tmp_path):
    assert load_stats(tmp_path / "nothing-here.json") == Stats()


@pytest.mark.parametrize(
    "contents",
    [
        "",
        "not json {",
        "[1, 2, 3]",
        '{"played": 3}',
        '{"version": 1, "played": -1, "won": 0, "current_streak": 0, "longest_streak": 0}',
        '{"version": 1, "played": 2, "won": 5, "current_streak": 0, "longest_streak": 0}',
        '{"version": 1, "played": 5, "won": 3, "current_streak": 3, "longest_streak": 2}',
        '{"version": 1, "played": 5, "won": 3, "current_streak": 0, "longest_streak": 4}',
        '{"version": 1, "played": "5", "won": 3, "current_streak": 0, "longest_streak": 1}',
        '{"version": 1, "played": 5.5, "won": 3, "current_streak": 0, "longest_streak": 1}',
        '{"version": 1, "played": true, "won": 0, "current_streak": 0, "longest_streak": 0}',
    ],
)
def test_r8_a_damaged_file_starts_fresh_instead_of_crashing(tmp_path, contents):
    path = tmp_path / "stats.json"
    path.write_text(contents)
    assert load_stats(path) == Stats()


def test_r8_saving_replaces_the_old_file_and_leaves_no_temporary_files(tmp_path):
    path = tmp_path / "stats.json"
    save_stats(play("W"), path)
    save_stats(play("WW"), path)
    assert load_stats(path).won == 2
    assert [p.name for p in tmp_path.iterdir()] == ["stats.json"]


def test_r8_stats_are_saved_in_the_home_directory_outside_the_repo():
    path = default_stats_path()
    assert path.name == ".wordle_stats.json"
    assert path.parent == path.home()
