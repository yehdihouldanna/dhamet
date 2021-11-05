# Dhamet Project

this project is an implementation of Dhamet which is a traditionnal Mauritanian Board game.

The rules are based 

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
        1. '+' nodes : nodes who's available directions are only horizontal or vertical
        2. '*' nodes : nodes who's available directoins are horizonatal vertical and dioganl (both dioganals included)



The end conditions are multiple :
    1. if one of the players score gets reduced to zero.
    2. if one of the players have no available moves
    3. if the game goes on for so long without a change in score.



For the UI we are going to use React :


