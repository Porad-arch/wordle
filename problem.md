# Problem

People who enjoy word puzzles want a quick way to challenge themselves and improve
their vocabulary. However, many online word games have distractions, advertisements,
daily limits, or require an internet connection.

# Initial requirements

- R1. Allow players to guess a hidden five-letter word.
- R2. Give players six attempts to guess the correct word.
- R3. Show which letters are correct and in the correct position, correct but in the
  wrong position, or not in the word.
- R4. Select a new random word for each game from a built-in word list.
- R5. Tell the player when they win or run out of attempts.
- R6. Reveal the correct word when the player loses.

# Round 2 requirements

- R7. Track the total number of games played, games won, and games lost, and
  calculate the player's win percentage.
- R8. Track the player's current and longest winning streak, and save these
  statistics locally so they persist between sessions.

# Round 3 requirements

- R2 (changed). Previously the player always had six attempts. The player now
  chooses Easy, Normal, or Hard before a game starts: Easy gives 8 guesses,
  Normal gives 6, and Hard gives 4.
- R9. Rate every word in the built-in list for difficulty, combining three
  things: whether the word has a repeated letter, whether it contains
  uncommon letters, and a hand-assigned rating of how common the word is.
  Easy games draw from the easiest words, Normal from the middle, and Hard
  from the hardest.

# Round 4 requirements

- R9 (changed). Calculate word difficulty primarily based on word commonness,
  with J, Q, X, and Z treated as uncommon letters. Uncommon-letter bonuses
  must not outweigh the word's overall commonness rating.

# Round 5 requirements

- R10. Track and display how many guesses it takes the player to win,
  including a distribution showing how many games were won in 1, 2, 3, 4, 5,
  6, 7, or 8 guesses.
