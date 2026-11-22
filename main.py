"""The terminal front end: reads guesses, prints the board, says who won,
and shows the running statistics after each game. With --reset-stats it
asks whether to clear the saved statistics instead (R11).

All the rules live in game.py, words.py, and stats.py. This file only handles
input and output. The only tests for it are of --reset-stats, in
tests/test_main.py.
"""

import sys

from game import Game, Mark, parse_difficulty, result_message
from stats import (
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
    average = average_guesses_to_win(stats)
    print(f"Average guesses to win {'-' if average is None else f'{average:.1f}'}")
    print()
    print("Guesses to win")
    counts = stats.wins_by_guesses
    for guesses, (count, length) in enumerate(zip(counts, bar_lengths(counts)), 1):
        bar = "#" * length + " " if length else ""
        print(f"  {guesses} | {bar}{count}")
    old = untracked_wins(stats)
    if old:
        noun = "win" if old == 1 else "wins"
        print(f"  (plus {old} earlier {noun} from before guess counts were kept)")


def ask_difficulty():
    """Ask for the level until the answer is understood. None means quit."""
    while True:
        try:
            raw = input("Difficulty? (e)asy, (n)ormal, (h)ard [n]: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        level = parse_difficulty(raw)
        if level is not None:
            return level
        print("  Please type e, n, or h (or press Enter for normal).")


def play_one(level, use_color):
    """Play one game at `level`. Returns (game, quit_early)."""
    game = Game(pick_word(difficulty=level), level.attempts)

    print(f"{level.name.title()}: guess the five-letter word.")
    print(f"You have {level.attempts} tries.  + right place   ? wrong place   . not in word")
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


def ask_reset(path):
    """Show the saved stats and clear them if the player says yes (R11)."""
    stats = load_stats(path)
    if stats.played == 0:
        print("No saved statistics to reset.")
        return 0
    show_stats(stats)
    print()
    try:
        answer = input("Reset all statistics? This cannot be undone. (y/N): ")
    except (EOFError, KeyboardInterrupt):
        print()
        return 0  # no answer is a no
    if not confirms_reset(answer):
        return 0
    try:
        reset_stats(path)
    except OSError as error:
        print(f"(Could not delete {path}: {error})")
        return 1
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    use_color = "--no-color" not in argv
    path = default_stats_path()
    if "--reset-stats" in argv:
        return ask_reset(path)  # never goes on to play
    stats = load_stats(path)

    while True:
        level = ask_difficulty()
        if level is None:
            return 0  # no game started, so nothing to record
        print()
        game, quit_early = play_one(level, use_color)
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
