# 0005. The three levels are equal thirds of the ranked word list

- Status: accepted
- Round: 3
- Requirement: R9

## Decision

In the context of **R9's "Easy games draw from the easiest words, Normal
from the middle, and Hard from the hardest"**,

facing **many words with the same score, and the need to draw the lines
between levels somewhere**,

we decided for **sorting every word by `(score, word)`, so ties are broken
alphabetically, and cutting that ranking into three nearly equal parts.
For the 100-word list that is 33, 33, and 34 words, with Hard getting the
extra one**,

and neglected **fixed score cut-offs (for example 1–2 Easy, 3–4 Normal, 5+
Hard)**,

to achieve **every level always having about a third of the words, so no
level is left with a handful of answers that repeat, even as the list or the
ratings change**,

accepting **that words with the same score can end up on two different
levels because of where they fall in the alphabet. For example, score-2
words are split between Easy and Normal, and score-3 words between Normal
and Hard.**

## Notes

- Chosen by the project owner at the start of round 3.
- The tests check that Easy's highest score is no higher than Normal's
  lowest, and the same for Normal and Hard, so the order of the levels can't
  be broken without a test failing.
