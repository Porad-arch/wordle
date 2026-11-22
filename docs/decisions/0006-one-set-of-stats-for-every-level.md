# 0006. One shared set of statistics for every level

- Status: accepted
- Round: 3
- Requirements: R2, R7, R8

## Decision

In the context of **round 3 adding Easy, Normal, and Hard levels on top of
round 2's saved statistics**,

facing **whether a win on Easy should count the same as a win on Hard**,

we decided for **keeping one set of played, won, and streak numbers that every
level counts toward, with the stats file format and `version` left as
they are**,

and neglected **separate statistics for each level, which would have needed
stats file version 2 and code to move version 1 numbers under Normal**,

to achieve **no risk to stats files players already have, and no change to
`stats.py` or its tests**,

accepting **that a streak can be built on Easy and then shown as if it were
earned on Hard, and that the stats can't show how a player does on each
level**.

## Notes

- Chosen by the project owner at the start of round 3.
- If a later round wants stats for each level, follow CLAUDE.md: bump
  `version`, keep reading version 1, and add a test that an old file loads.
