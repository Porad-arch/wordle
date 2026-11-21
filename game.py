"""Game rules for the word-guessing game.

Everything in this module is pure logic: no printing, no input, no randomness.
That is deliberate, so every rule can be tested by calling a function and
checking what it returns.
"""

from enum import Enum

WORD_LENGTH = 5
MAX_ATTEMPTS = 6


class Mark(Enum):
    """How one letter of a guess scored."""

    CORRECT = "correct"  # right letter, right position
    PRESENT = "present"  # letter is in the word, but somewhere else
    ABSENT = "absent"  # letter is not in the word at all


def score_guess(guess, answer):
    """Score `guess` against `answer`, returning one Mark per letter.

    A letter is only ever credited once. If the answer has one E and the guess
    has two, exactly one of them scores; the other is ABSENT. Letters in the
    right position are claimed first, which is why this takes two passes.
    """
    guess = guess.upper()
    answer = answer.upper()
    if len(guess) != len(answer):
        raise ValueError(
            f"guess has {len(guess)} letters but the answer has {len(answer)}"
        )

    marks = [Mark.ABSENT] * len(guess)

    # First pass: exact positions win, and the letters they use up are not
    # available to anything else.
    unclaimed = {}
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            marks[i] = Mark.CORRECT
        else:
            unclaimed[a] = unclaimed.get(a, 0) + 1

    # Second pass: remaining letters may claim what is left over.
    for i, g in enumerate(guess):
        if marks[i] is Mark.CORRECT:
            continue
        if unclaimed.get(g, 0) > 0:
            marks[i] = Mark.PRESENT
            unclaimed[g] -= 1

    return marks


class Game:
    """One play-through: the hidden answer plus the guesses made so far."""

    def __init__(self, answer, max_attempts=MAX_ATTEMPTS):
        answer = answer.upper()
        if len(answer) != WORD_LENGTH or not answer.isalpha():
            raise ValueError(f"answer must be {WORD_LENGTH} letters: {answer!r}")
        self.answer = answer
        self.max_attempts = max_attempts
        self.guesses = []  # list of (guess, list-of-Mark)

    @property
    def attempts_used(self):
        return len(self.guesses)

    @property
    def attempts_left(self):
        return self.max_attempts - self.attempts_used

    @property
    def is_won(self):
        return any(word == self.answer for word, _ in self.guesses)

    @property
    def is_lost(self):
        return not self.is_won and self.attempts_left <= 0

    @property
    def is_over(self):
        return self.is_won or self.is_lost

    def guess(self, word):
        """Record one guess and return its marks.

        Raises ValueError if the guess is the wrong shape, or if the game has
        already finished.
        """
        if self.is_over:
            raise ValueError("the game is already over")

        word = word.strip().upper()
        if len(word) != WORD_LENGTH:
            raise ValueError(f"a guess must be exactly {WORD_LENGTH} letters")
        if not word.isalpha():
            raise ValueError("a guess must be letters only")

        marks = score_guess(word, self.answer)
        self.guesses.append((word, marks))
        return marks


def result_message(game):
    """The line shown when the game ends, or None if it is still running."""
    if game.is_won:
        return (
            f"You got it in {game.attempts_used} of {game.max_attempts} guesses!"
        )
    if game.is_lost:
        return f"Out of guesses. The word was {game.answer}."
    return None
