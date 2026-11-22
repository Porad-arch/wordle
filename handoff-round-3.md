# Handoff after round 3

For the session that does round 4. Read `CLAUDE.md` first for the standing
rules. This file covers only what is true now and what came out of round 3.

## Current state

- Branch `main`, pushed to `origin/main`. The last round 3 commit is `ad9538e`.
  The working tree was clean apart from this file and a `CLAUDE.md` change
  that the owner has not yet reviewed.
- `problem.md` has R1–R6 (round 1), R7–R8 (round 2), and round 3's changed
  R2 and new R9. **There are no round 4 requirements yet.** They have to come
  from the project owner and go into `problem.md`, committed and pushed,
  before any other round 4 work.
- `python3 -m pytest` gives **121 passed**, with nothing skipped:

  | File | Tests | Requirements |
  |---|---|---|
  | `tests/test_game.py` | 47 | R1, R2, R3, R5, R6 |
  | `tests/test_words.py` | 37 | R4, R9 |
  | `tests/test_stats.py` | 37 | R7, R8 (unchanged in round 3) |

- Round 3 is done. Changed R2 (Easy 8, Normal 6, Hard 4 guesses, chosen
  before every game) and R9 (every word rated, and each level draws from its
  third of the list) are implemented, tested, and described in `spec.md`
  under "Round 3". The README describes the levels.

### Files

| File | What changed in round 3 |
|---|---|
| `game.py` | New `Difficulty` enum (`EASY`, `NORMAL`, `HARD`) with `.attempts`, and `parse_difficulty(text)`. `MAX_ATTEMPTS` is now `Difficulty.NORMAL.attempts` (still 6). |
| `words.py` | `COMMONNESS` (word → hand rating 1–3) is now the word list. `WORDS = list(COMMONNESS)`. New: `UNCOMMON_LETTERS`, `has_repeated_letter`, `uncommon_letter_count`, `difficulty_score`, `ranked_words`, `words_for(difficulty)`. `pick_word(rng=None, difficulty=None)`. |
| `stats.py` | Unchanged. The stats file is still `"version": 1`. |
| `main.py` | New `ask_difficulty()`, which asks before every game. `play_one(level, use_color)` takes the level. |
| `tests/test_game.py` | The old fixed-six R2 tests were replaced with tests for the three levels and for `parse_difficulty`. |
| `tests/test_words.py` | New R9 tests. |
| `docs/decisions/0004–0006` | New. |

### How the levels split today

| Level | Guesses | Words | Scores in it |
|---|---|---|---|
| Easy | 8 | 33 | 25 words scoring 1, 8 scoring 2 |
| Normal | 6 | 33 | 27 words scoring 2, 6 scoring 3 |
| Hard | 4 | 34 | 17 words scoring 3, 11 scoring 4, 5 scoring 5, 1 scoring 6 |

## How to run it

    python3 main.py              # play: pick a level, then guess
    python3 main.py --no-color   # without ANSI colours
    python3 -m pytest            # all tests

Requires Python 3 and `pytest`, nothing else.

**To try the game by hand without touching your real statistics**, point
`HOME` at a scratch folder:

    HOME=$(mktemp -d) python3 main.py

**To force a known answer while trying it out** (this changes nothing on
disk). You still choose the level at the prompt, and it still sets the number
of guesses:

    HOME=$(mktemp -d) python3 -c "import main; main.pick_word=lambda difficulty=None: 'CRANE'; main.main([])"

**The round 2 handoff's version, `main.pick_word=lambda: 'CRANE'`, no longer
works.** `main.py` now calls `pick_word(difficulty=level)`, so a stand-in
that takes no arguments crashes with `TypeError` as soon as the first game
starts. The stand-in must accept the `difficulty` keyword. Both commands are
also in the Commands section of `CLAUDE.md`.

## Decisions made in round 3, and why

Four were asked of the project owner before any code was written. The rest
were made during the round and reported to the owner at the end.

**Chosen by the project owner:**

1. **A word's score is a plain sum.** It is 1 if the word has a repeated
   letter, plus 1 for each uncommon letter each time it appears, plus the
   hand rating (1 everyday, 2 familiar, 3 less common). Higher is harder.
   Anyone can check it by hand. See `docs/decisions/0004`.
2. **The uncommon letters are `J Q X Z K V W Y F B`.** These were proposed
   in the question and the owner accepted them. They are a rule of thumb
   from English letter frequency.
3. **The levels are equal thirds of the ranked list** (sorted by score, ties
   alphabetical), not fixed score cut-offs. This way no level ends up with
   only a few words. See `docs/decisions/0005`.
4. **All levels share one set of statistics.** The file format is
   unchanged, so nobody's stats are at risk. See `docs/decisions/0006`.
5. **The level is asked before every game**, and Enter means Normal.

**Made during the round (not asked for, but reported to the owner):**

6. **The round 3 session assigned the 1–3 commonness ratings for all 100
   words.** CRANE 1, PIZZA 2, and JEWEL 3 were set to match the example the
   owner approved. The rest are that session's judgement. **The owner has
   not reviewed them.**
7. **`COMMONNESS` is the word list** and `WORDS` is built from it, so a word
   can't be added without a rating. The order of the list is unchanged, so
   the old seeded `pick_word` results are the same.
8. **When the list doesn't divide by three, Hard gets the extra words.**
9. **Words with the same score can land on two levels** because of the
   alphabetical tie-break (see the table above).
10. **`Difficulty` and `parse_difficulty` live in `game.py`** so they can be
    tested. Each level's enum value is its number of guesses.
11. **The level question accepts `e`/`easy`, `n`/`normal`, `h`/`hard`** in
    any case, with spaces trimmed. Anything else prints a hint and asks again.
12. **Ctrl-C or end of input at the level question exits without recording a
    game.** No game has started, the same as at "Play again?".
13. **`MAX_ATTEMPTS` stays 6, and `Game(answer)` with no count still gives
    6** (Normal), so round 1 code and tests keep working.
14. **`pick_word()` with no level still picks from the whole list**, so R4
    and its tests are unchanged.
15. **The game names the level when it starts**, for example
    "Hard: guess the five-letter word."
16. Out of scope, and listed in `spec.md`: separate stats for each level,
    a command-line flag for the level, and changing the level mid-game.

## Unresolved / candidates for later rounds

- **The owner should review the commonness ratings in `words.py`.** Some
  results may look odd. HAPPY and HONEY are on Hard because of the Y and the
  repeated letter. Score-2 words early in the alphabet (BREAD, CHAIN, CREAM)
  are on Easy while later ones are on Normal.
- **Each level has only about 33 answers**, so the same word comes up again
  far sooner than with 100. Nothing stops the same word twice in a row. A
  bigger word list or "don't repeat recent words" would need a requirement.
- **There are no stats for each level** (decision 0006). Adding them needs a
  file format change (see the warnings).
- **The level can't be set from the command line.**
- From earlier rounds, still not done: checking that a guess is a real word,
  a reset command, counts of how many guesses each win took, more than one
  player, a warning when a damaged stats file is reset, and two copies of the
  game overwriting each other's save.

## Warnings for the next session

- **Three commits don't pass on their own**, because tests were committed
  before the code on purpose: `65b839a` (round 2), and `03bac62` and
  `d172966` (round 3). Every other commit passes. If you bisect, skip them.
  Don't try to fix them: commits are never amended.
- **`words.py` imports `Difficulty` from `game.py`.** `game.py` must never
  import `words.py`, or the import becomes circular.
- **`Difficulty`'s values are the guess counts** (8, 6, 4). If a change gives
  two levels the same count, Python's `Enum` silently makes the second an
  alias of the first, and `list(Difficulty)` loses a level. If that ever
  happens, give the levels separate values and store the count as a separate
  attribute.
- **`words_for` assumes exactly three levels.** It divides by a literal 3
  and uses each level's position in `list(Difficulty)`. Adding or reordering
  levels changes which words go where, so update it and its tests together.
- **Changing one rating or adding one word can move other words between
  levels**, because the cuts are by rank. The R9 tests check the rules of the
  split, not which level a given word is on, except for CRANE (Easy) and
  JEWEL (Hard).
- **Don't reorder `pick_word`'s parameters.** `test_r4_…` calls
  `pick_word(random.Random(7))` with the generator as its first argument.
- **The stats file is still version 1, and players depend on it.** Per
  `CLAUDE.md`: a format change must bump `version`, keep reading version 1,
  and add a test that a version 1 file still loads. Adding a `Stats` field
  also means updating `FIELDS` and `_from_dict` in `stats.py`, and
  `test_r8_the_file_holds_all_the_statistics`.
- **`main.py` has no tests**, by design. Round 3's prompt flow (asking
  again, Enter meaning Normal, quitting at the prompt recording nothing) was
  checked by hand only, with a scratch `HOME`.
- **Decision records go up to 0006.** The next one is `0007`.
