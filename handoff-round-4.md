# Handoff after round 4

For the session that does round 5. Read `CLAUDE.md` first for the standing
rules. This file covers only what is true now and what came out of round 4.

## Current state

- Branch `main`, pushed to `origin/main`. The last round 4 commit is
  `b061dfe`. The working tree was clean apart from this file (and any
  `CLAUDE.md` change made with it), which the owner has not yet reviewed.
- `problem.md` has R1–R6 (round 1), R7–R8 (round 2), round 3's changed R2
  and new R9, and round 4's changed R9. **There are no round 5 requirements
  yet.** They have to come from the project owner and go into `problem.md`,
  committed and pushed, before any other round 5 work.
- `python3 -m pytest` gives **139 passed**, with nothing skipped:

  | File | Tests | Requirements |
  |---|---|---|
  | `tests/test_game.py` | 47 | R1, R2, R3, R5, R6 (unchanged in round 4) |
  | `tests/test_words.py` | 55 | R4, R9 |
  | `tests/test_stats.py` | 37 | R7, R8 (unchanged in round 4) |

- Round 4 is done. The changed R9 is implemented, tested, and described in
  `spec.md` under "Round 4". The README describes the new rule.

### Round 4 commits

| Commit | What |
|---|---|
| `cda4783` | Round 4 requirement in `problem.md` (committed before the session started) |
| `ab6a8e9` | `spec.md` Round 4 section |
| `7e5e1f3` | Uncommon letters narrowed to J, Q, X, Z |
| `776163c` | Score becomes a `(rating, bonus)` pair, rating first |
| `ce42fb7` | README explains the new rule |
| `b061dfe` | Decision record 0007, and 0004 marked "replaced in part" |

Every round 4 commit passes on its own. Between `7e5e1f3` and `776163c`
the code is a half-way state: it still uses the round 3 sum, but with only
four uncommon letters. That matches neither round's spec, but its tests pass.

### Files

| File | What changed in round 4 |
|---|---|
| `words.py` | `UNCOMMON_LETTERS = frozenset("JQXZ")`. New `letter_bonus(word)` (J/Q/X/Z each time they appear, plus 1 for a repeated letter). `difficulty_score(word)` now returns the pair `(COMMONNESS[word], letter_bonus(word))`, not an int. `COMMONNESS`, `ranked_words`, `words_for`, and `pick_word` are unchanged. |
| `tests/test_words.py` | R9 tests rewritten for the pair and the four letters. New tests: K/V/W/Y/F/B add nothing, a less common word beats a more common one for every pair of words, PIZZA ranks below every rated-3 word, the bonus still orders words with the same rating, and each level's ratings are in order. |
| `docs/decisions/0007` | New. `0004`'s Status line now says it is replaced in part by 0007. |
| `spec.md`, `README.md` | Round 4 described. |
| `game.py`, `stats.py`, `main.py` | Unchanged. The stats file is still `"version": 1`. |

### How the levels split today

| Level | Guesses | Words | Pairs in it |
|---|---|---|---|
| Easy | 8 | 33 | 33 × (1, 0) |
| Normal | 6 | 33 | 4 × (1, 0), 11 × (1, 1), 18 × (2, 0) |
| Hard | 4 | 34 | 10 × (2, 0), 10 × (2, 1), 1 × (2, 3), 9 × (3, 0), 3 × (3, 1), 1 × (3, 2) |

All 13 words rated 3 are on Hard. Everyday words (rated 1) are never on Hard.

## How to run it

    python3 main.py              # play: pick a level, then guess
    python3 main.py --no-color   # without ANSI colours
    python3 -m pytest            # all tests

Requires Python 3 and `pytest`, nothing else. To try it by hand without
touching the real stats, and optionally with a known answer, use the two
commands in the Commands section of `CLAUDE.md` (scratch `HOME`, and a
`pick_word` stand-in that accepts `difficulty=`). Both were used in round 4
and still work.

## Decisions made in round 4, and why

**Chosen by the project owner** (asked before any code was written):

1. **The rating always wins.** A bonus can't lift a word level with, let
   alone above, a word with a higher commonness rating. "Must not outweigh"
   was read in its strictest form.
2. **The repeated-letter point stays**, under the same rule: it only orders
   words with the same rating. R9 (changed) doesn't mention it, so it was
   asked.
3. **J, Q, X, Z count each time they appear** (PIZZA has 2), as in round 3.
4. **The 1–3 hand ratings are unchanged**, and the levels are still equal
   thirds (decision 0005).

**Made during the round (not asked for, reported to the owner):**

5. **The score is a `(rating, bonus)` pair, compared rating first.** I chose
   this over `10 × rating + bonus` and over a capped sum, so the guarantee
   doesn't depend on the bonus staying small. See `docs/decisions/0007`.
6. **A new function, `letter_bonus(word)`**, so the bonus can be tested
   apart from the rating.
7. **Decision 0004's Status line was edited** to point at 0007. Only that
   line changed. The owner may prefer old records left untouched.
8. **The change was split into two passing commits** (letters, then
   ordering) rather than committing tests first.
9. **Some round 3 R9 tests were replaced, not kept.** The test that averaged
   scores now averages ratings (pairs can't be averaged). The worked examples
   changed: JEWEL now has 1 uncommon letter (was 2), and QUICK has 1 (was 2).
10. **The new tests were checked against the round 3 scoring** in a scratch
    copy. The rule-defining tests fail there (8 failures), so they really
    test the change.
11. **The README's difficulty paragraph was rewritten.** The owner didn't
    ask for that.
12. **Listed as out of scope in `spec.md`:** changing ratings or the 1–3
    scale, and changing the equal-thirds split.

## Unresolved / candidates for later rounds

- **The owner still hasn't reviewed the commonness ratings** in `words.py`.
  The round 3 session assigned them. Since round 4 they decide almost
  everything about which level a word is on, so a wrong rating now matters
  more than before.
- **The alphabetical tie-break pushes some everyday words onto Normal.**
  Easy has room for only 33 of the 37 everyday words with no bonus. The four
  that come last alphabetically (VOICE, WATCH, WATER, WORDS) are on Normal
  while the same kind of word is on Easy. Rated-2 words with no bonus are
  split between Normal and Hard the same way. Within a tie, a word late in
  the alphabet always goes to the harder level. Fixing this would mean
  changing decision 0005 (fixed cut-offs, or a different tie-break), which
  needs the owner.
- **The letter bonus can never move a word across a boundary the ratings
  already decide.** It only matters inside the Easy/Normal and Normal/Hard
  overlaps. If the owner expected J/Q/X/Z to make more difference, the
  requirement would have to change.
- **Each level has about 33 answers**, and nothing stops the same word twice
  in a row (from round 3).
- From earlier rounds, still not done: stats for each level, setting the
  level from the command line, checking that a guess is a real word, a reset
  command, counts of how many guesses each win took, more than one player, a
  warning when a damaged stats file is reset, and two copies of the game
  overwriting each other's save.

## Warnings for the next session

- **`difficulty_score` returns a tuple now, not an int.** Anything that adds,
  averages, or prints it as a number breaks. `sorted`, `max`, `min`, and
  `<` work. To average, use `COMMONNESS[w]` or `letter_bonus(w)`.
- **Bisect:** the commits that don't pass on their own are still the three
  from earlier rounds: `65b839a` (round 2), and `03bac62` and `d172966`
  (round 3). Round 4 added none. Don't try to fix them.
- **Changing one rating can move other words between levels**, because the
  cuts are by rank. The R9 tests check the rules of the split, not which
  level a word is on, except CRANE (Easy) and JEWEL (Hard). The new test
  that every pair of words is ordered by rating is about 10,000 comparisons.
  It is fast at 100 words but grows with the square of the list.
- **Warnings from round 3 still hold:**
  - `words.py` imports `Difficulty` from `game.py`, never the reverse.
  - `Difficulty`'s values are the guess counts (8, 6, 4). Two equal counts
    would silently make one level an alias of another.
  - `words_for` assumes exactly three levels.
  - Don't reorder `pick_word`'s parameters (`test_r4_…` passes the
    generator first).
  - The stats file is version 1. A format change must bump `version`, keep
    reading version 1, and add a test that an old file loads.
  - `main.py` has no tests. Round 4 didn't change it. It was played by hand
    with a scratch `HOME`.
- **Decision records go up to 0007.** The next one is `0008`.
