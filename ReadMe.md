
# Dhamet (Traditional Mauritanian board game) AI Project

## Introduction

This project is an implementation of Dhamet which is a traditionnal Mauritanian board game.
it's in the same family of board games such as checkers and such but goes back way before theses variants even existed,

## Some of the main functionalities in the project : 
- It contains all the basic rules of the game,
- you can play against other players or against the AI,
- It contains also bots that simulate human behavior ( when the players waits for a while before another player could join him)
- ... It contains many other interesting functionalities.

Some ressources that inspired the way this code is made are :
[Nguyen, Dung & Wong, Stephen. (2002). Design patterns for games. ACM Sigcse Bulletin. 34. 126-130. 10.1145/563340.563387.](https://www.researchgate.net/publication/221537302_Design_patterns_for_games/citation/download)

The rules are adapted by relying on this magazine: [Jeux et Stratégie, no 27, juin-juillet 1984, p. 46-48](http://fr.1001mags.com/parution/jeux-strategie/numero-27-jun-jui-1984)

## Mathematical majoration of the number of the possible moves in the game

Given that the game has 81 quares with each squares having 5 possible states (corresponding to the type of the piece it contains ({regular,dhaima}x{white,black} or empty)),
and each postition have two players to move,
and that at each position we can have 5 states (either player win =2 , draw by blockade, or draw by repetition)
and that we have to oblige a rule of 50_moves of non killing max (elsewise the game could go forever 'repetition')

then we can majorate the number of the possible moves with an upper bound as follows :
$$ NumberofMoves < 81^{5} \times 2 \times 5 \times 50 ≈ 1.7 \times 10^{12} $$
So the number of moves in Dhamet 40 is less than <font color ="red"> $1.7 \times 10^{12}$ </font>which makes it -computationnaly speaking- much simpler than chess ($≈ 2\times10^{76}$)

## The technologies used in this Project are 

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![image](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
![image](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)

-    `Python` , `Django` : For the back end and the game code and AI agents

-    `SQLite3` , For the data storage and access,

-    `React JS`, `JavaScript`,`Bootstrap`, `CSS3` for the front end user web page.
  
-    `Rest_framework` & `web-pack` : for the linking between both ends.

-    `Channels` : which is a python library that allows for asynchronous communication
                  it's a way to simplify the code of `websockets` in django projects.
                  so that 2 players can play the game online against each other.


### The structure of the project :

The project is mainly a Django Project that links multiple apps :

The result of the tree command (simplified) is as follows :
```shell
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

**DhametFront** : is the Django project's entry :

**React_UI**    : is the app who is in charge of rendering the game to user on the browser,

**DhametCode**  : it is the app who is in charge of the game in the back end, it is also where the game's data is architectured and accessed,

### Some crucial implementation details : 
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


### Extra details :

- The **console version** of the game is a standalone dependency and can be executed by itself just : 
```shell
cd DhametCode/utils && python Board.py
```  
it does print the board elegantly on the console and could be played by itself.

- The database could be changed in the future base on demand and needs so the `SQLite3` that is used can be replaced.

- On the React-UI there are two ways to move the pieces :
    * Drag and drop (not recommended, because dragging diagonaly generates a little bit of interference with the adjacent cells
    so this functionnality still needs maintenence).

    * Click-DoubleClick (recommended): you can select a piece by clicking it, once selected you can click on the moves you want to perform and double click on the last one in order to signal the intent of ending your turn.

### Some Util commands for devellopement: 

to start the `django` porject type in :```shell 
python manage.py runserver ```
To compile the updated react component in the React_UI app u have to use teh web pack configuration so just type in the terminal :

```shell 
npm run dev 
```


 **To Start the redis-cli**
first start the redis server (in another terminal) with    
```shell 
redis-server
```
Then start redis-cli as follows (assuming that the installation folder is located here)

```shell
cd "C:\\Program Files\\Redis" ; "redis-cli"
```
or with arguments as follows

```shell
cd "C:\\Program Files\\Redis" &
".\redis-cli -h localhost -p6379"
```


### git commands (hard) :
to merge recursively while favoring the current local branch with another branch foo 
```shell
git merge -s recursive -X ours foo
git merge -s recursive -X ours origin/interface
```

to update the historic of git locally

git fetch --all

and then each contributor will have to pull from his computer to update his/her code
with ```git pull```

if it doesn't work,
we fetch and manuallly merge with master

```shell
git fetch --all
git merge -X theirs origin/master

or for more forcing
git merge -X theirs origin/master
```

to merge a branch into master :



# Global server 
python .\manage.py runserver 0.0.0.0:8000




# Online Server Deploy :

digital ocean machine IP adress:
165.22.85.224

to connect to the digital machine :
open a git bash : 
and type the following command:
ssh  root@165.22.85.224
ssh  yehdih@165.22.85.224


https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04

   ╭───────────────────────────────────────────────────────────────╮
   │                                                               │
   │      This is a cool ASCII art container that I found          │
   │               and wanted to keep                              │
   │                                                               │
   │                                                               │
   ╰───────────────────────────────────────────────────────────────╯
