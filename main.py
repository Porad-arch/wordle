"""The terminal front end: reads guesses, prints the board, says who won.

All the rules live in game.py. This file only handles input and output, which
is why there are no tests for it.
"""

import sys

from game import MAX_ATTEMPTS, Game, Mark, result_message
from words import pick_word

SYMBOL = {Mark.CORRECT: "+", Mark.PRESENT: "?", Mark.ABSENT: "."}
COLOR = {
    Mark.CORRECT: "\033[42;30m",  # green background
    Mark.PRESENT: "\033[43;30m",  # yellow background
    Mark.ABSENT: "\033[47;30m",  # grey background
}
RESET = "\033[0m"


def render(word, marks, use_color=True):
    """Two lines: the letters, and a symbol under each one."""
    if use_color:
        letters = "".join(f"{COLOR[m]} {c} {RESET}" for c, m in zip(word, marks))
    else:
        letters = "".join(f" {c} " for c in word)
    symbols = "".join(f" {SYMBOL[m]} " for m in marks)
    return f"  {letters}\n  {symbols}"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    use_color = "--no-color" not in argv

    game = Game(pick_word())

    print("Guess the five-letter word.")
    print(f"You have {MAX_ATTEMPTS} tries.  + right place   ? wrong place   . not in word")
    print()

    while not game.is_over:
        prompt = f"Guess {game.attempts_used + 1}/{game.max_attempts}: "
        try:
            raw = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print(f"\nStopping. The word was {game.answer}.")
            return 0

        try:
            marks = game.guess(raw)
        except ValueError as error:
            print(f"  {error}")
            continue

        print(render(game.guesses[-1][0], marks, use_color))
        print()

    print(result_message(game))
    return 0


if __name__ == "__main__":
    sys.exit(main())
