"""Tests for the game rules. Each test names the requirement it checks."""

import pytest

from game import MAX_ATTEMPTS, Game, Mark, result_message, score_guess

C = Mark.CORRECT
P = Mark.PRESENT
A = Mark.ABSENT


# R1: Allow players to guess a hidden five-letter word.


def test_r1_a_five_letter_guess_is_recorded():
    game = Game("CRANE")
    game.guess("SLATE")
    assert game.guesses[0][0] == "SLATE"
    assert game.attempts_used == 1


def test_r1_guess_is_case_insensitive_and_trimmed():
    game = Game("CRANE")
    game.guess("  slate ")
    assert game.guesses[0][0] == "SLATE"


@pytest.mark.parametrize("bad", ["CAT", "SLATES", "", "SLAT3", "SL TE"])
def test_r1_guesses_that_are_not_five_letters_are_rejected(bad):
    game = Game("CRANE")
    with pytest.raises(ValueError):
        game.guess(bad)
    assert game.attempts_used == 0


# R2: Give players six attempts to guess the correct word.


def test_r2_six_attempts_by_default():
    assert MAX_ATTEMPTS == 6
    assert Game("CRANE").attempts_left == 6


def test_r2_attempts_run_out_after_six_wrong_guesses():
    game = Game("CRANE")
    for _ in range(6):
        game.guess("STONE")
    assert game.attempts_used == 6
    assert game.attempts_left == 0
    assert game.is_over


def test_r2_a_seventh_guess_is_refused():
    game = Game("CRANE")
    for _ in range(6):
        game.guess("STONE")
    with pytest.raises(ValueError):
        game.guess("CRANE")


# R3: Show which letters are correct and in the correct position, correct but
#     in the wrong position, or not in the word.


def test_r3_exact_match_is_all_correct():
    assert score_guess("CRANE", "CRANE") == [C, C, C, C, C]


def test_r3_no_shared_letters_is_all_absent():
    assert score_guess("MUDDY", "CRANE") == [A, A, A, A, A]


def test_r3_right_letter_wrong_place_is_present():
    # CRANE contains A and E, but not in these positions.
    assert score_guess("AUDIE", "CRANE") == [P, A, A, A, C]


def test_r3_extra_copies_of_a_letter_are_absent():
    # THESE has exactly two E's. Guessing five of them must not light up five:
    # the two in the right places score, the other three get nothing.
    assert score_guess("EEEEE", "THESE") == [A, A, C, A, C]


def test_r3_both_copies_score_when_the_answer_has_two():
    # SPEED has two E's, so both E's in the guess are allowed to score.
    assert score_guess("ERASE", "SPEED") == [P, A, A, P, P]


def test_r3_a_letter_in_the_right_place_is_claimed_first():
    # ABBEY has two B's. BOBBY offers three: the one in position 3 lines up,
    # one more scores as present, and the extra gets nothing.
    assert score_guess("BOBBY", "ABBEY") == [P, A, C, A, C]


def test_r3_mismatched_lengths_are_an_error():
    with pytest.raises(ValueError):
        score_guess("CAT", "CRANE")


# R5: Tell the player when they win or run out of attempts.


def test_r5_winning_is_detected_and_reported():
    game = Game("CRANE")
    game.guess("STONE")
    game.guess("CRANE")
    assert game.is_won
    assert game.is_over
    assert not game.is_lost
    assert "2 of 6" in result_message(game)


def test_r5_losing_is_detected_and_reported():
    game = Game("CRANE")
    for _ in range(6):
        game.guess("STONE")
    assert game.is_lost
    assert game.is_over
    assert not game.is_won
    assert "Out of guesses" in result_message(game)


def test_r5_no_result_message_while_the_game_is_running():
    game = Game("CRANE")
    game.guess("STONE")
    assert result_message(game) is None


# R6: Reveal the correct word when the player loses.


def test_r6_the_answer_appears_in_the_losing_message():
    game = Game("CRANE")
    for _ in range(6):
        game.guess("STONE")
    assert "CRANE" in result_message(game)


def test_r6_the_answer_is_not_revealed_when_the_player_wins():
    game = Game("CRANE")
    game.guess("CRANE")
    # The win message congratulates; it must not read like the reveal.
    assert "The word was" not in result_message(game)
