"""Tests for the built-in word list (R4) and its difficulty ratings (R9)."""

import random

import pytest

from game import WORD_LENGTH, Difficulty
from words import (
    COMMONNESS,
    UNCOMMON_LETTERS,
    WORDS,
    difficulty_score,
    has_repeated_letter,
    letter_bonus,
    pick_word,
    ranked_words,
    uncommon_letter_count,
    words_for,
)


# R4: Select a new random word for each game from a built-in word list.


def test_r4_every_word_in_the_list_is_five_uppercase_letters():
    bad = [w for w in WORDS if len(w) != WORD_LENGTH or not w.isalpha() or w != w.upper()]
    assert bad == []


def test_r4_the_list_has_no_duplicates():
    assert len(WORDS) == len(set(WORDS))


def test_r4_the_list_is_big_enough_to_be_worth_playing():
    assert len(WORDS) >= 50


def test_r4_pick_word_returns_a_word_from_the_list():
    for _ in range(50):
        assert pick_word() in WORDS


def test_r4_pick_word_is_repeatable_with_a_seeded_generator():
    # Same seed, same word. This is what lets a test control the answer.
    assert pick_word(random.Random(7)) == pick_word(random.Random(7))


def test_r4_pick_word_does_not_always_return_the_same_word():
    # A "random" choice that never varies would pass every test above.
    seen = {pick_word() for _ in range(200)}
    assert len(seen) > 1


# R9 (changed in round 4): rate every word for difficulty, primarily by how
#     common it is, with J, Q, X, and Z as uncommon letters. Letter bonuses
#     must not outweigh the commonness rating. Easy games draw from the
#     easiest words, Normal from the middle, and Hard from the hardest.


def test_r9_every_word_has_a_hand_rating_from_1_to_3():
    assert set(COMMONNESS) == set(WORDS)
    assert all(COMMONNESS[w] in (1, 2, 3) for w in WORDS)


def test_r9_every_hand_rating_value_is_used():
    # A rating that is always the same number would add nothing to the score.
    assert set(COMMONNESS.values()) == {1, 2, 3}


@pytest.mark.parametrize(
    "word, repeated",
    [("CRANE", False), ("PIZZA", True), ("JEWEL", True), ("APPLE", True), ("SLATE", False)],
)
def test_r9_repeated_letters_are_detected(word, repeated):
    assert has_repeated_letter(word) is repeated


def test_r9_the_uncommon_letters_are_j_q_x_and_z():
    assert UNCOMMON_LETTERS == frozenset("JQXZ")


@pytest.mark.parametrize("word", ["KNEES", "VOICE", "WATCH", "STORY", "FIELD", "BREAD"])
def test_r9_k_v_w_y_f_and_b_no_longer_count_as_uncommon(word):
    assert uncommon_letter_count(word) == 0


@pytest.mark.parametrize(
    "word, count",
    [("CRANE", 0), ("PIZZA", 2), ("JEWEL", 1), ("QUICK", 1), ("INDEX", 1), ("JUICE", 1)],
)
def test_r9_uncommon_letters_are_counted_each_time_they_appear(word, count):
    assert uncommon_letter_count(word) == count


@pytest.mark.parametrize(
    "word, bonus",
    [("CRANE", 0), ("HAPPY", 1), ("QUICK", 1), ("JEWEL", 2), ("PIZZA", 3)],
)
def test_r9_the_letter_bonus_adds_uncommon_letters_and_a_repeat(word, bonus):
    assert letter_bonus(word) == bonus


def test_r9_the_letter_bonus_is_the_sum_for_every_word():
    for w in WORDS:
        assert letter_bonus(w) == uncommon_letter_count(w) + int(has_repeated_letter(w))


@pytest.mark.parametrize(
    "word, score", [("CRANE", (1, 0)), ("HAPPY", (1, 1)), ("PIZZA", (2, 3)), ("JEWEL", (3, 2))]
)
def test_r9_the_score_is_the_rating_then_the_bonus(word, score):
    assert difficulty_score(word) == score


def test_r9_the_score_puts_the_rating_first_for_every_word():
    for w in WORDS:
        assert difficulty_score(w) == (COMMONNESS[w], letter_bonus(w))


def test_r9_a_less_common_word_is_always_harder_whatever_its_letters():
    # The heart of the round 4 change: no bonus lifts a word level with, or
    # above, a word whose rating is higher.
    for a in WORDS:
        for b in WORDS:
            if COMMONNESS[a] < COMMONNESS[b]:
                assert difficulty_score(a) < difficulty_score(b), (a, b)


def test_r9_pizza_ranks_below_every_less_common_word():
    # In round 3 PIZZA (familiar, but Z, Z and a repeat) outranked every
    # less common word. Its letters must no longer outweigh its rating.
    ranked = ranked_words()
    rated_3 = [w for w in WORDS if COMMONNESS[w] == 3]
    assert all(ranked.index("PIZZA") < ranked.index(w) for w in rated_3)


def test_r9_the_bonus_still_orders_words_with_the_same_rating():
    # "Primarily" by commonness, not only: the letters still count.
    assert difficulty_score("HAPPY") > difficulty_score("CRANE")
    assert difficulty_score("PIZZA") > difficulty_score("SALAD")


def test_r9_the_score_is_case_insensitive():
    assert difficulty_score("pizza") == difficulty_score("PIZZA")


def test_r9_ranked_words_holds_every_word_once_easiest_first():
    ranked = ranked_words()
    assert sorted(ranked) == sorted(WORDS)
    scores = [difficulty_score(w) for w in ranked]
    assert scores == sorted(scores)


def test_r9_ties_are_broken_alphabetically():
    ranked = ranked_words()
    for a, b in zip(ranked, ranked[1:]):
        if difficulty_score(a) == difficulty_score(b):
            assert a < b


def test_r9_the_three_levels_split_the_list_with_nothing_left_over():
    easy, normal, hard = (set(words_for(d)) for d in Difficulty)
    assert easy | normal | hard == set(WORDS)
    assert not (easy & normal or normal & hard or easy & hard)


def test_r9_the_levels_are_nearly_equal_thirds():
    sizes = [len(words_for(d)) for d in Difficulty]
    assert sum(sizes) == len(WORDS)
    assert max(sizes) - min(sizes) <= 1


def test_r9_easy_words_score_no_higher_than_normal_and_normal_than_hard():
    easy, normal, hard = ([difficulty_score(w) for w in words_for(d)] for d in Difficulty)
    assert max(easy) <= min(normal)
    assert max(normal) <= min(hard)


def test_r9_the_easiest_and_hardest_words_land_on_the_right_level():
    assert "CRANE" in words_for(Difficulty.EASY)
    assert "JEWEL" in words_for(Difficulty.HARD)


def test_r9_hard_words_are_less_common_on_average_than_easy_words():
    def mean_rating(ws):
        return sum(COMMONNESS[w] for w in ws) / len(ws)

    assert mean_rating(words_for(Difficulty.EASY)) < mean_rating(words_for(Difficulty.NORMAL))
    assert mean_rating(words_for(Difficulty.NORMAL)) < mean_rating(words_for(Difficulty.HARD))


def test_r9_easy_ratings_are_no_higher_than_normal_and_normal_than_hard():
    easy, normal, hard = ([COMMONNESS[w] for w in words_for(d)] for d in Difficulty)
    assert max(easy) <= min(normal)
    assert max(normal) <= min(hard)


@pytest.mark.parametrize("level", list(Difficulty))
def test_r9_pick_word_draws_only_from_the_chosen_level(level):
    allowed = set(words_for(level))
    rng = random.Random(3)
    for _ in range(200):
        assert pick_word(rng, difficulty=level) in allowed


@pytest.mark.parametrize("level", list(Difficulty))
def test_r9_pick_word_varies_within_a_level(level):
    rng = random.Random(5)
    assert len({pick_word(rng, difficulty=level) for _ in range(200)}) > 1
