# +-------------------------------------------------------------------------------------+
# |<<<<<<<<<<<<<<<<<                 Dhamet AI Project                 >>>>>>>>>>>>>>>> |
# +-------------------------------------------------------------------------------------+


# Introduction :

This project is an implementation of Dhamet which is a traditionnal Mauritanian board game.
it's in the same family of board games such as checkers and such but goes back way before theses variants.

Some ressources that inspired the way this code is made are : 
    - 
[Nguyen, Dung & Wong, Stephen. (2002). Design patterns for games. ACM Sigcse Bulletin. 34. 126-130. 10.1145/563340.563387.](https://www.researchgate.net/publication/221537302_Design_patterns_for_games/citation/download)

The rules are adapted by relying on this magazine: [Jeux et Stratégie, no 27, juin-juillet 1984, p. 46-48](http://fr.1001mags.com/parution/jeux-strategie/numero-27-jun-jui-1984)


# The technologies used in this Project are : 
'   `Python` , `Django` : For the back end and the game code and AI agents
    `SQLite3` , For the data storage and access,
    `React JS`, `JavaScript`,`Bootstrap`, `CSS3` for the front end user web page.
    `Rest_framework` : for the linking between both ends.

# The structure of the project :

The project is mainly a Django Project that links multiple apps :

The result of the tree command (simplified) is as follows :
```Python 
Project Folder:.
├───DhametCode
│   ├───migrations
│   ├───templates
│   ├───utils
├───DhametFront
├───React_UI
│   ├───migrations
│   ├───node_modules
│   ├───src
│   │   └───components
│   ├───static
│   │   ├───css
│   │   ├───frontend
│   │   └───images
│   ├───templates
│   │   └───frontend
├───Therory_sources
├───uploads
    └───images
```
From which we can see the three main apps of the project :

**DhametFront** : is the Django project entry :

**React_UI**    : is the app of the project that is charge of rendering the game to user on the browser,

**DhametCode**  : it is the app in charge of the game in the back end, it is also were the games data set is architectured and communicated with,

# Some crucial implementation details : 
The game is represented by a state, this state have for now in the code two representations :

- The first representation is  *a 9x9 matrix* : containing :

        * 1 if the piece is a regular white piece.

        * 3 if the piece is a 'Dhaima' white piece.

        * -1 if the piece is a regular black piece.

        * -3 if the piece is Black 'Dhaima' piece.

        * 0 if there is no piece.


        Example(Initial Game State):
```Python
        board0=[
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  0, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1,]]
```
        
    
- The second representation is *an 81 long string* containing :

        * w if the piece is a regular white piece.

        * W if the piece is a 'Dhaima' white piece.

        * b if the piece is a regular black piece.

        * B if the piece is Black 'Dhaima' piece.

        * _ if there is no piece.

        Example(Initial Game State):
```Python
        board0 = """wwwwwwwww
                    wwwwwwwww
                    wwwwwwwww
                    wwwwwwwww
                    wwww_bbbb
                    bbbbbbbbb
                    bbbbbbbbb
                    bbbbbbbbb
                    bbbbbbbbb"""
```
'

The bone method of the implementation on the back end side is the *move* method, which requires the knowledge of allowed moves at a given state of the game from **available_moves** method and does the move if it is allowed elsewise it return a boolean equal to False.

In the available moves function the logic is to base on the matrix representation of the game state and to follow the possible directions by relying on vectors. (~unit vectors: ([1,1] is considered unitary here ^_^))
'
**There are 2 types of nodes** each of which have specific conditions to possible moves:

    * 1. `+` : nodes who's available directions are only horizontal or vertical.

    * 2. `*` : nodes who's available directions are horizontal vertical and diogonal (both diagonals included)


**The end conditions are multiple :**
    * 1. if one of the players' gets opponenet `score reduced to zero`.

    * 2. if one of the players have `no available moves`

    * 3. if the game goes on for `so long without a change in score`.(this is a customisable condition.)


# Extra details :

- The **console version** of the game is a standalone dependency and can be executed by itself just : 
**`cd DhametCode/utils && python Board.py`**  it does print the board elegantly on the console and could be played by itself.

- The database could be changed in the future base on demand and needs so the `SQLite3` that is used can be replaced.

- On the React-UI there are two ways to move the pieces :
    * Drag and drop (not recommended, because dragging diagonaly generates a little bit of interference with the adjacent cells
    so this functionnality still needs maintenence).

    * Click-DoubleClick (recommended): you can select a piece by clicking it, once selected you can click on the moves you want to perform and double click on the last one in order to signal the intent of ending your turn.



