"""Tests for the built-in word list (R4)."""

import random

from game import WORD_LENGTH
from words import WORDS, pick_word


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
