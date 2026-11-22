"""The terminal front end: reads guesses, prints the board, says who won,
and shows the running statistics after each game.

All the rules live in game.py. This file only handles input and output, which
is why there are no tests for it.
"""

import sys

from game import MAX_ATTEMPTS, Game, Mark, result_message
from stats import default_stats_path, load_stats, record_game, save_stats, win_percentage
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


def show_stats(stats):
    print(
        f"Played {stats.played}   Won {stats.won}   Lost {stats.lost}   "
        f"Win {win_percentage(stats)}%"
    )
    print(f"Current streak {stats.current_streak}   Longest streak {stats.longest_streak}")


def play_one(use_color):
    """Play one game. Returns (game, quit_early)."""
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
            return game, True

        try:
            marks = game.guess(raw)
        except ValueError as error:
            print(f"  {error}")
            continue

        print(render(game.guesses[-1][0], marks, use_color))
        print()

    print(result_message(game))
    return game, False


def ask_play_again():
    try:
        answer = input("Play again? (y/n): ")
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer.strip().lower() in ("y", "yes")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    use_color = "--no-color" not in argv
    path = default_stats_path()
    stats = load_stats(path)

    while True:
        game, quit_early = play_one(use_color)
        stats = record_game(stats, game)
        try:
            save_stats(stats, path)
        except OSError as error:
            print(f"(Could not save statistics to {path}: {error})")
        print()
        show_stats(stats)
        print()
        if quit_early or not ask_play_again():
            return 0
        print()


if __name__ == "__main__":
    sys.exit(main())
