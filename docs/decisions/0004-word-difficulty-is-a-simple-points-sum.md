# 0004. A word's difficulty is a simple sum of points

- Status: replaced in part by 0007 in round 4 (the plain sum and the ten
  uncommon letters no longer apply; the hand rating and the repeated-letter
  point are kept)
- Round: 3
- Requirement: R9

## Decision

In the context of **R9, which asks for every word to be rated by combining a
repeated letter, uncommon letters, and a hand-assigned commonness rating**,

facing **no rule in the requirement for how the three parts weigh against
each other, or which letters count as uncommon**,

we decided for **an unweighted sum: 1 point if the word has a repeated
letter, 1 point for each uncommon letter each time it appears (from
`J Q X Z K V W Y F B`), plus a hand rating of 1 (everyday), 2 (familiar), or
3 (less common)**,

and neglected **doubling the hand rating so how common the word is counts
most, and counting uncommon letters only once per word (yes or no)**,

to achieve **a score anyone can work out in their head and check against the
code, where every part can move a word up or down a level**,

accepting **that the weights are a judgement call rather than measured, that
a word with several uncommon letters (PIZZA, JEWEL) can outrank one that is
simply rare, and that the ten-letter set is a rule of thumb from English
letter frequency, not from data about this list**.

## Alternatives considered

| Option | Why not |
|---|---|
| `2 × commonness` + the letter parts | Makes the hand rating dominate. The two letter checks would rarely change a word's level. |
| Uncommon letters as yes/no | PIZZA (two Z's) would score the same as a word with a single K. Repeats of a hard letter would be ignored. |

## Notes

- Chosen by the project owner at the start of round 3.
- The hand ratings are in `COMMONNESS` in `words.py`. The session that did
  round 3 assigned them. The owner may want to review them. Changing a rating
  can move a word to a different level, and the tests will still pass as long
  as the split rules hold.
