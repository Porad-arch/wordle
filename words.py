"""The built-in word list, so the game needs no internet connection (R4),
and each word's difficulty rating (R9)."""

import random

from game import Difficulty

# How common each word is, rated by hand (R9):
#   1 = everyday, 2 = familiar, 3 = less common.
# This dictionary is the word list: WORDS below is made from it.
COMMONNESS = {
    "CRANE": 1, "SLATE": 2, "AUDIO": 2, "HOUSE": 1, "PLANT": 1,
    "MONEY": 1, "WATER": 1, "LIGHT": 1, "NIGHT": 1, "PHONE": 1,
    "TABLE": 1, "CHAIR": 1, "BREAD": 1, "SUGAR": 1, "SPICE": 2,
    "TRAIN": 1, "BRAIN": 1, "CHAIN": 2, "GRAPE": 2, "APPLE": 1,
    "LEMON": 2, "MANGO": 2, "BERRY": 2, "CLOUD": 1, "STORM": 2,
    "SHINE": 2, "BEACH": 1, "RIVER": 1, "STONE": 1, "EARTH": 1,
    "OCEAN": 1, "FIELD": 2, "GRASS": 1, "FLOOR": 1, "SMILE": 1,
    "LAUGH": 1, "DREAM": 1, "SLEEP": 1, "DRINK": 1, "SNACK": 2,
    "PIZZA": 2, "SALAD": 2, "STEAK": 2, "HONEY": 2, "CREAM": 2,
    "JUICE": 1, "TOAST": 2, "CANDY": 2, "MUSIC": 1, "DANCE": 1,
    "PIANO": 2, "DRUMS": 2, "FLUTE": 3, "VOICE": 1, "SOUND": 1,
    "NOISE": 2, "QUIET": 2, "PEACE": 2, "HAPPY": 1, "ANGRY": 1,
    "TIRED": 1, "ALERT": 3, "SMART": 2, "BRAVE": 2, "QUICK": 2,
    "SHARP": 2, "ROUGH": 2, "CLEAN": 1, "DIRTY": 2, "FRESH": 2,
    "STALE": 3, "SWEET": 1, "SALTY": 2, "HEART": 1, "HANDS": 1,
    "TEETH": 2, "KNEES": 3, "ELBOW": 3, "THUMB": 2, "WRIST": 3,
    "SHIRT": 1, "PANTS": 1, "SHOES": 1, "SOCKS": 2, "SCARF": 3,
    "GLOVE": 2, "WATCH": 1, "CROWN": 3, "JEWEL": 3, "PAPER": 1,
    "PENNY": 3, "BOOKS": 1, "NOVEL": 3, "STORY": 1, "POEMS": 3,
    "WORDS": 1, "LABEL": 2, "TITLE": 2, "PAGES": 2, "INDEX": 3,
}

WORDS = list(COMMONNESS)

# Letters that make a word harder to find (R9, changed in round 4 to just
# these four). Each one adds a point every time it appears in the word.
UNCOMMON_LETTERS = frozenset("JQXZ")


def has_repeated_letter(word):
    word = word.upper()
    return len(set(word)) < len(word)


def uncommon_letter_count(word):
    return sum(1 for c in word.upper() if c in UNCOMMON_LETTERS)


def letter_bonus(word):
    """Extra difficulty from the letters: J, Q, X, Z each time they appear,
    plus 1 if any letter is repeated."""
    return uncommon_letter_count(word) + int(has_repeated_letter(word))


def difficulty_score(word):
    """A (rating, bonus) pair. Higher is harder.

    Pairs compare first item first, so the hand commonness rating always
    decides, and the letter bonus only orders words with the same rating.
    However big the bonus, it can never outweigh the rating (R9, round 4).
    """
    word = word.upper()
    return (COMMONNESS[word], letter_bonus(word))


def ranked_words():
    """Every word, easiest first. Ties are broken alphabetically so the
    order, and so each level's words, never changes from run to run."""
    return sorted(WORDS, key=lambda w: (difficulty_score(w), w))


def words_for(difficulty):
    """The words a level draws from: Easy the first third of the ranking,
    Normal the middle third, and Hard the last. When the list doesn't divide
    evenly, Hard gets the extra words."""
    ranked = ranked_words()
    n = len(ranked)
    i = list(Difficulty).index(difficulty)
    return ranked[i * n // 3 : (i + 1) * n // 3]


def pick_word(rng=None, difficulty=None):
    """Return a random word: from the given level's words, or from the whole
    list if no level is given.

    `rng` can be a seeded random.Random for tests, so the choice is
    repeatable when we need it to be.
    """
    chooser = rng if rng is not None else random
    pool = WORDS if difficulty is None else words_for(difficulty)
    return chooser.choice(pool)
