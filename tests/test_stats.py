"""Tests for game statistics (R7), saved streaks (R8), and the distribution
of winning guess counts (R10), and resetting the saved statistics (R11)."""

import json

import pytest

from game import Difficulty, Game
from stats import (
    GUESS_ROWS,
    Stats,
    average_guesses_to_win,
    bar_lengths,
    confirms_reset,
    default_stats_path,
    load_stats,
    record_game,
    reset_stats,
    save_stats,
    untracked_wins,
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
        "version": 2,
        "played": 3,
        "won": 2,
        "current_streak": 0,
        "longest_streak": 2,
        "wins_by_guesses": [2, 0, 0, 0, 0, 0, 0, 0],
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


# R10: Track and display how many guesses it takes the player to win,
#      including a distribution showing how many games were won in 1, 2, 3,
#      4, 5, 6, 7, or 8 guesses.


def won_in(guesses, level=Difficulty.EASY):
    """A game won on the given guess, at a level with enough guesses."""
    game = Game("CRANE", level.attempts)
    for _ in range(guesses - 1):
        game.guess("STONE")
    game.guess("CRANE")
    return game


def record_all(games, stats=None):
    stats = Stats() if stats is None else stats
    for game in games:
        stats = record_game(stats, game)
    return stats


def row(guesses, count=1):
    """A distribution with `count` wins in the given number of guesses."""
    counts = [0] * 8
    counts[guesses - 1] = count
    return tuple(counts)


def test_r10_there_is_a_row_for_each_of_1_to_8_guesses():
    assert GUESS_ROWS == 8
    assert len(Stats().wins_by_guesses) == 8


def test_r10_every_level_fits_in_the_distribution():
    assert all(level.attempts <= GUESS_ROWS for level in Difficulty)


def test_r10_a_new_player_has_no_wins_in_any_row():
    assert Stats().wins_by_guesses == (0, 0, 0, 0, 0, 0, 0, 0)


@pytest.mark.parametrize("guesses", range(1, 9))
def test_r10_a_win_counts_in_the_row_for_its_number_of_guesses(guesses):
    stats = record_game(Stats(), won_in(guesses))
    assert stats.wins_by_guesses == row(guesses)


def test_r10_a_loss_adds_nothing_to_the_distribution():
    assert record_game(Stats(), lost_game()).wins_by_guesses == row(1, 0)


def test_r10_a_quit_game_adds_nothing_to_the_distribution():
    assert record_game(Stats(), quit_game()).wins_by_guesses == row(1, 0)


def test_r10_wins_add_up_in_their_rows():
    stats = record_all(
        [won_in(3), won_in(4), lost_game(), won_in(3), won_in(8), won_in(1)]
    )
    assert stats.wins_by_guesses == (1, 0, 2, 1, 0, 0, 0, 1)
    assert sum(stats.wins_by_guesses) == stats.won


def test_r10_every_level_counts_toward_the_same_distribution():
    stats = record_all(
        [
            won_in(2, Difficulty.HARD),
            won_in(2, Difficulty.NORMAL),
            won_in(2, Difficulty.EASY),
        ]
    )
    assert stats.wins_by_guesses == row(2, 3)


def test_r10_recording_a_win_does_not_change_the_old_distribution():
    before = record_game(Stats(), won_in(3))
    record_game(before, won_in(3))
    assert before.wins_by_guesses == row(3)


def test_r10_a_new_player_has_no_untracked_wins():
    assert untracked_wins(record_all([won_in(2), lost_game(), won_in(5)])) == 0


def test_r10_untracked_wins_are_wins_not_in_the_distribution():
    stats = Stats(played=10, won=7, wins_by_guesses=row(4, 3))
    assert untracked_wins(stats) == 4


def test_r10_no_average_before_any_win():
    assert average_guesses_to_win(Stats()) is None
    assert average_guesses_to_win(record_game(Stats(), lost_game())) is None


def test_r10_average_of_one_win_is_its_guess_count():
    assert average_guesses_to_win(record_game(Stats(), won_in(4))) == 4.0


@pytest.mark.parametrize(
    "guesses, expected",
    [
        ([2, 3, 3], 2.7),  # 8 / 3 = 2.666...
        ([1, 2], 1.5),
        ([1, 1, 2], 1.3),  # 4 / 3 = 1.333...
        ([1] * 19 + [2], 1.1),  # 21 / 20 = 1.05, half rounds up
        ([3, 4, 5, 6], 4.5),
    ],
)
def test_r10_average_is_rounded_to_one_decimal_place(guesses, expected):
    stats = record_all(won_in(g) for g in guesses)
    assert average_guesses_to_win(stats) == expected


def test_r10_average_leaves_out_untracked_wins():
    # 5 old wins with no guess count, then two new wins in 2 and 4.
    old = Stats(played=5, won=5, current_streak=5, longest_streak=5)
    stats = record_all([won_in(2), won_in(4)], old)
    assert average_guesses_to_win(stats) == 3.0


def test_r10_bars_are_one_mark_per_win_when_they_fit():
    assert bar_lengths((0, 1, 5, 8, 4, 1, 0, 0)) == [0, 1, 5, 8, 4, 1, 0, 0]


def test_r10_the_biggest_bar_is_cut_to_the_width():
    assert bar_lengths((0, 0, 40, 20, 10, 0, 0, 0), width=20) == [
        0, 0, 20, 10, 5, 0, 0, 0,
    ]


def test_r10_scaled_bars_round_halves_up():
    # 3 * 20 / 40 = 1.5, so it rounds up to 2.
    assert bar_lengths((3, 40), width=20) == [2, 20]


def test_r10_a_row_with_any_wins_keeps_a_visible_bar():
    assert bar_lengths((1, 1000), width=20) == [1, 20]


def test_r10_no_wins_means_no_bars():
    assert bar_lengths((0,) * 8) == [0] * 8


def test_r10_the_distribution_is_saved_and_loads_back(tmp_path):
    path = tmp_path / "stats.json"
    stats = record_all([won_in(3), won_in(3), won_in(6), lost_game(), won_in(1)])
    save_stats(stats, path)
    loaded = load_stats(path)
    assert loaded == stats
    assert loaded.wins_by_guesses == (1, 0, 2, 0, 0, 1, 0, 0)


def test_r10_an_old_version_1_file_still_loads(tmp_path):
    path = tmp_path / "stats.json"
    path.write_text(
        '{"version": 1, "played": 12, "won": 9, '
        '"current_streak": 3, "longest_streak": 5}'
    )
    stats = load_stats(path)
    assert (stats.played, stats.won) == (12, 9)
    assert (stats.current_streak, stats.longest_streak) == (3, 5)
    assert stats.wins_by_guesses == row(1, 0)
    assert untracked_wins(stats) == 9


def test_r10_an_old_file_is_saved_as_version_2_after_the_next_game(tmp_path):
    path = tmp_path / "stats.json"
    path.write_text(
        '{"version": 1, "played": 2, "won": 1, '
        '"current_streak": 1, "longest_streak": 1}'
    )
    save_stats(record_game(load_stats(path), won_in(5)), path)
    data = json.loads(path.read_text())
    assert data["version"] == 2
    assert (data["played"], data["won"]) == (3, 2)
    assert data["wins_by_guesses"] == [0, 0, 0, 0, 1, 0, 0, 0]
    assert untracked_wins(load_stats(path)) == 1


V2 = '{{"version": 2, "played": 5, "won": 3, "current_streak": 1, "longest_streak": 2{}}}'


@pytest.mark.parametrize(
    "extra",
    [
        "",  # no distribution at all
        ', "wins_by_guesses": null',
        ', "wins_by_guesses": "0,1,2"',
        ', "wins_by_guesses": [0, 1, 2, 0, 0, 0, 0]',  # 7 rows
        ', "wins_by_guesses": [0, 1, 2, 0, 0, 0, 0, 0, 0]',  # 9 rows
        ', "wins_by_guesses": [0, 1, -1, 0, 0, 0, 0, 0]',
        ', "wins_by_guesses": [0, 1.5, 0, 0, 0, 0, 0, 0]',
        ', "wins_by_guesses": [0, true, 0, 0, 0, 0, 0, 0]',
        ', "wins_by_guesses": [0, 2, 2, 0, 0, 0, 0, 0]',  # 4 wins, only 3 won
    ],
)
def test_r10_a_damaged_version_2_file_starts_fresh(tmp_path, extra):
    path = tmp_path / "stats.json"
    path.write_text(V2.format(extra))
    assert load_stats(path) == Stats()


def test_r10_a_good_version_2_file_loads(tmp_path):
    path = tmp_path / "stats.json"
    path.write_text(V2.format(', "wins_by_guesses": [0, 1, 2, 0, 0, 0, 0, 0]'))
    stats = load_stats(path)
    assert stats == Stats(5, 3, 1, 2, (0, 1, 2, 0, 0, 0, 0, 0))


# R11: resetting the saved statistics.


def played_stats():
    return Stats(3, 2, 1, 2, (0, 1, 1, 0, 0, 0, 0, 0))


@pytest.mark.parametrize("answer", ["y", "Y", "yes", "YES", "Yes", "  y  ", "yes\n"])
def test_r11_yes_confirms_the_reset(answer):
    assert confirms_reset(answer) is True


@pytest.mark.parametrize(
    "answer", ["", "   ", "n", "no", "N", "yep", "ye", "y y", "reset", "1"]
)
def test_r11_anything_but_yes_keeps_the_stats(answer):
    # The question defaults to No, so Enter on its own must not reset.
    assert confirms_reset(answer) is False


def test_r11_reset_deletes_the_stats_file(tmp_path):
    path = tmp_path / "stats.json"
    save_stats(played_stats(), path)
    reset_stats(path)
    assert not path.exists()


def test_r11_after_a_reset_the_stats_load_as_all_zeros(tmp_path):
    path = tmp_path / "stats.json"
    save_stats(played_stats(), path)
    reset_stats(path)
    assert load_stats(path) == Stats()


def test_r11_resetting_a_version_1_file_clears_its_untracked_wins(tmp_path):
    path = tmp_path / "stats.json"
    path.write_text(json.dumps(
        {"version": 1, "played": 3, "won": 2, "current_streak": 1, "longest_streak": 2}
    ))
    assert untracked_wins(load_stats(path)) == 2
    reset_stats(path)
    assert untracked_wins(load_stats(path)) == 0


def test_r11_resetting_with_no_file_is_not_an_error(tmp_path):
    path = tmp_path / "stats.json"
    reset_stats(path)
    reset_stats(path)  # twice in a row is fine too
    assert not path.exists()


def test_r11_reset_leaves_other_files_alone(tmp_path):
    path = tmp_path / "stats.json"
    other = tmp_path / "other.json"
    other.write_text("keep me")
    save_stats(played_stats(), path)
    reset_stats(path)
    assert other.read_text() == "keep me"


def test_r11_a_reset_that_cannot_delete_raises_oserror(tmp_path):
    # A folder where the stats file should be can't be removed as a file.
    path = tmp_path / "stats.json"
    path.mkdir()
    with pytest.raises(OSError):
        reset_stats(path)
    assert path.exists()


def test_r11_playing_after_a_reset_starts_from_zero(tmp_path):
    path = tmp_path / "stats.json"
    save_stats(played_stats(), path)
    reset_stats(path)
    save_stats(record_game(load_stats(path), won_game()), path)
    assert load_stats(path) == Stats(1, 1, 1, 1, (1, 0, 0, 0, 0, 0, 0, 0))
