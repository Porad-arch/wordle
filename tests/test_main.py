"""Tests for the --reset-stats command-line option (R11).

main.py is otherwise presentation and checked by hand. R11 is about a
command-line option, so these tests run main.main with the answers fed in
and the stats file pointed at a temporary directory, never the player's
real ~/.wordle_stats.json.
"""

import pytest

import main
from stats import Stats, load_stats, save_stats


@pytest.fixture
def stats_path(tmp_path, monkeypatch):
    path = tmp_path / "stats.json"
    monkeypatch.setattr(main, "default_stats_path", lambda: path)
    return path


@pytest.fixture
def answers(monkeypatch):
    """Feed typed answers to input(). End of input once they run out."""
    given = []
    prompts = []

    def fake_input(prompt=""):
        prompts.append(prompt)
        if not given:
            raise EOFError
        return given.pop(0)

    monkeypatch.setattr("builtins.input", fake_input)
    # Never start a real game with a random word.
    monkeypatch.setattr(main, "pick_word", lambda difficulty=None: "CRANE")
    return given, prompts


def saved(path):
    stats = Stats(5, 4, 2, 3, (0, 1, 2, 1, 0, 0, 0, 0))
    save_stats(stats, path)
    return stats


def test_r11_yes_deletes_the_saved_stats(stats_path, answers):
    given, _ = answers
    saved(stats_path)
    given.append("y")
    assert main.main(["--reset-stats"]) == 0
    assert not stats_path.exists()
    assert load_stats(stats_path) == Stats()


def test_r11_no_keeps_the_saved_stats(stats_path, answers):
    given, _ = answers
    stats = saved(stats_path)
    given.append("n")
    assert main.main(["--reset-stats"]) == 0
    assert load_stats(stats_path) == stats


def test_r11_enter_on_its_own_keeps_the_saved_stats(stats_path, answers):
    given, _ = answers
    stats = saved(stats_path)
    given.append("")
    main.main(["--reset-stats"])
    assert load_stats(stats_path) == stats


def test_r11_end_of_input_at_the_question_keeps_the_saved_stats(stats_path, answers):
    _, prompts = answers
    stats = saved(stats_path)
    assert main.main(["--reset-stats"]) == 0  # no answers given
    assert len(prompts) == 1 and "Reset all statistics?" in prompts[0]
    assert load_stats(stats_path) == stats


def test_r11_ctrl_c_at_the_question_keeps_the_saved_stats(stats_path, monkeypatch):
    stats = saved(stats_path)
    prompts = []

    def interrupted(prompt=""):
        prompts.append(prompt)
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", interrupted)
    assert main.main(["--reset-stats"]) == 0
    assert len(prompts) == 1 and "Reset all statistics?" in prompts[0]
    assert load_stats(stats_path) == stats


def test_r11_the_question_comes_before_anything_is_cleared(stats_path, answers):
    given, prompts = answers
    saved(stats_path)
    given.append("y")
    main.main(["--reset-stats"])
    assert len(prompts) == 1
    assert "Reset all statistics?" in prompts[0]
    assert "cannot be undone" in prompts[0]
    assert "(y/N)" in prompts[0]


def test_r11_the_current_stats_are_shown_before_the_question(stats_path, answers, capsys):
    given, _ = answers
    saved(stats_path)
    given.append("n")
    main.main(["--reset-stats"])
    out = capsys.readouterr().out
    assert "Played 5   Won 4   Lost 1" in out
    assert "Guesses to win" in out


def test_r11_the_option_does_not_start_a_game(stats_path, answers):
    given, prompts = answers
    saved(stats_path)
    given.extend(["n", "e", "CRANE", "n"])
    main.main(["--reset-stats"])
    assert not any("Difficulty?" in p for p in prompts)
    assert not any("Guess" in p for p in prompts)
    assert given == ["e", "CRANE", "n"]  # only the reset answer was read


def test_r11_with_nothing_saved_there_is_no_question(stats_path, answers, capsys):
    _, prompts = answers
    assert main.main(["--reset-stats"]) == 0
    assert prompts == []
    assert "No saved statistics to reset." in capsys.readouterr().out
    assert not stats_path.exists()


def test_r11_works_alongside_no_color(stats_path, answers):
    given, _ = answers
    saved(stats_path)
    given.append("yes")
    assert main.main(["--no-color", "--reset-stats"]) == 0
    assert not stats_path.exists()


def test_r11_a_reset_that_fails_says_so_and_exits_with_1(tmp_path, answers, monkeypatch, capsys):
    given, _ = answers
    path = tmp_path / "stats.json"
    saved(path)
    monkeypatch.setattr(main, "default_stats_path", lambda: path)

    def cannot_delete(p):
        raise PermissionError("read-only")

    monkeypatch.setattr(main, "reset_stats", cannot_delete, raising=False)
    given.append("y")
    assert main.main(["--reset-stats"]) == 1
    assert str(path) in capsys.readouterr().out
    assert path.exists()


def test_r11_without_the_option_the_stats_are_not_reset(stats_path, answers):
    # A guard, not a check of new code: the old program passes it too.
    given, _ = answers
    stats = saved(stats_path)
    given.append("y")  # not a level, so the game asks again, then end of input
    main.main([])
    assert load_stats(stats_path) == stats
