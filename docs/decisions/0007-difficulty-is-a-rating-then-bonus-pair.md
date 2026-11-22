# 0007. A word's difficulty is a (rating, bonus) pair, compared rating first

- Status: accepted
- Round: 4
- Requirement: R9 (changed)
- Replaces in part: 0004 (the plain sum and the ten uncommon letters)

## Decision

In the context of **R9 changed in round 4: difficulty is "primarily based
on word commonness", J, Q, X, and Z are the uncommon letters, and
"uncommon-letter bonuses must not outweigh the word's overall commonness
rating"**,

facing **the owner's choice that the rating must always win (a bonus may
not even bring a word level with a less common one), and the question of
how to make that hold in the code rather than just usually hold**,

we decided for **`difficulty_score(word)` returning a pair,
`(COMMONNESS[word], letter_bonus(word))`, where the bonus is J/Q/X/Z each
time they appear plus 1 for a repeated letter, and relying on Python
comparing pairs first item first**,

and neglected **a weighted number such as `10 × rating + bonus`, and a
plain sum with the bonus capped below one rating step**,

to achieve **a guarantee that doesn't depend on a magic weight or on how
big the bonus can get. Adding a letter rule later, or longer words, can't
quietly let a bonus overtake the rating. `ranked_words`, `words_for`, and
the level tests work on pairs unchanged.**

accepting **that the score is no longer one number you can add up in your
head or average, so a test that averaged scores now averages ratings, and
that the bonus can only move a word within its own rating's place in the
ranking, never across a level boundary that the ratings already decide**.

## Alternatives considered

| Option | Why not |
|---|---|
| `10 × rating + bonus` (CRANE 10, PIZZA 23, JEWEL 32) | Reads as one number, but only works while the bonus stays below 10. That limit lives in a constant someone has to remember. |
| Plain sum, bonus capped below 1 (for example a fraction of a point) | Same result for ordering, but fractional scores are harder to read and the cap is another rule to keep in step. |

## Notes

- The owner chose at the start of round 4: the rating always wins, the
  repeated-letter point stays (under the same rule), J/Q/X/Z count each time
  they appear, and the hand ratings are unchanged. The pair is how this
  session put that into code.
- Ties within the same pair are still broken alphabetically, and the levels
  are still equal thirds (0005).
