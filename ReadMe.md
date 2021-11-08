# Dhamet Project

This project is an implementation of Dhamet which is a traditionnal Mauritanian Board game.
it's in the same family of board games such as checkers and such.

Some ressources that inspired the way this code is made are : 
    [Nguyen, Dung & Wong, Stephen. (2002). Design patterns for games. ACM Sigcse Bulletin. 34. 126-130. 10.1145/563340.563387.](https://www.researchgate.net/publication/221537302_Design_patterns_for_games/citation/download)


The game State is represented by a 9x9 matrix containing :
    1 if the piece is a regular white piece.
    3 if the piece is a 'Dhaima' white piece.
    -1 if the piece is a regular black piece.
    -3 if the piece is Black 'Dhaima' piece.
    0 if there is no piece.

In the available moves function :
    the logic is to follow the possible directions by relying on vectors. (~unit vectors: ([1,1] is considered unitary here ^_^))

Also the there are 2 types of nodes:
    1. `+` nodes : nodes who's available directions are only horizontal or vertical.
    2. `*` nodes : nodes who's available directoins are horizonatal vertical and diogonal (both diagonals included)

# TO START THE CONSOLE VERSION OF THE GAME :
run the Board.py file with the following command in a terminal or a command prompt.
`python Board.py`

The end conditions are multiple :
    1. if one of the players' gets opponenet `score reduced to zero`.
    2. if one of the players have `no available moves`
    3. if the game goes on for `so long without a change in score`.(this is a customisable condition.)



For the UI we are going to use `React` :
    the drag and drop and drop functionnnality is based on the `React-dnd` library this library needs a backend for it to function,
    for now we are using the `HTML5Backend` for starters, but it's possibel to change it to `touch` for mobile devices version.


