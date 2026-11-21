"""The built-in word list, so the game needs no internet connection (R4)."""

import random

WORDS = [
    "CRANE", "SLATE", "AUDIO", "HOUSE", "PLANT",
    "MONEY", "WATER", "LIGHT", "NIGHT", "PHONE",
    "TABLE", "CHAIR", "BREAD", "SUGAR", "SPICE",
    "TRAIN", "BRAIN", "CHAIN", "GRAPE", "APPLE",
    "LEMON", "MANGO", "BERRY", "CLOUD", "STORM",
    "SHINE", "BEACH", "RIVER", "STONE", "EARTH",
    "OCEAN", "FIELD", "GRASS", "FLOOR", "SMILE",
    "LAUGH", "DREAM", "SLEEP", "DRINK", "SNACK",
    "PIZZA", "SALAD", "STEAK", "HONEY", "CREAM",
    "JUICE", "TOAST", "CANDY", "MUSIC", "DANCE",
    "PIANO", "DRUMS", "FLUTE", "VOICE", "SOUND",
    "NOISE", "QUIET", "PEACE", "HAPPY", "ANGRY",
    "TIRED", "ALERT", "SMART", "BRAVE", "QUICK",
    "SHARP", "ROUGH", "CLEAN", "DIRTY", "FRESH",
    "STALE", "SWEET", "SALTY", "HEART", "HANDS",
    "TEETH", "KNEES", "ELBOW", "THUMB", "WRIST",
    "SHIRT", "PANTS", "SHOES", "SOCKS", "SCARF",
    "GLOVE", "WATCH", "CROWN", "JEWEL", "PAPER",
    "PENNY", "BOOKS", "NOVEL", "STORY", "POEMS",
    "WORDS", "LABEL", "TITLE", "PAGES", "INDEX",
]


def pick_word(rng=None):
    """Return a random word from the built-in list.

    `rng` can be a seeded random.Random for tests, so the choice is
    repeatable when we need it to be.
    """
    chooser = rng if rng is not None else random
    return chooser.choice(WORDS)
