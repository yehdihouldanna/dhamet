*This is a non exhaustive list of features and functionnalities that will be added to the game. as we progress the need to add more elements to this list might raise up.*

- **[Crucial]** Add animations. animating the game pieces based on movements and events of take and soufflé etc...
    - animating pieces appeareances; [-/]
    - animating pieces movements.  [ ]
    - animating pieces disapearances (taken of the board).


- **[Crucial]** Improve the interface of the Web page. (Buy a game template for it.)
    - improve the game background and the style of the pieces.
    - Improve players banner.
    - Add a button for resign , draw and new game.

- **[Very_Importent]** Add a timer functionnality. (add a timer for each player and limited typed game options)
    - sync the timer between both fronts and
    - set the ground truth for the timer in the back-end,
    - set time win condition.
    - 

- Add sound effects SFX to the game.

- Migrate the database to postgres instead of sqlite.

- Refractor the code in favor of Fat models Skinny views (a recommended Django practice) . 

- Make it possible to render a previous game state from historic by clicking on it.

- Clean improve and modelise player's profile and stats.

- Update the documentation with images based on the actual game.

- Add on first sign in tool tip tutorials on how to play the game.

- Add a chat functionnality so that the players can chat while playing.

- Tournament Feature. (add a features that queues multiple players and pair them in a tournament set up)

- Authentication with google,facebook APIs. (add a social authentication based on the Auth2 api of google and facebook)

- Extra AI levels and make them use soufflé too. ( inceased AI difficulty options )

- Add An AI based on machine learning ,(after data collection train an AI based on the data.).

- Add an AI based on reinforcement learning.

- Move the functional code to the front end. ( Move the logic of the game to the front end. to increase the performance.)

- Add more specifications for each type of dhamet, (3 , 12 , 40 )


### Current Bugs:

- Sign up before sign in. --> Inverse the two.

- Player can't take a soufflé if the oppoenent last move closed the soufflé valid taking point., --> make soufflé to be based on the previous turn's game state instead of the current.

- Ai wins before the game actually ends.
To reproduce the bug : 
```Python
33 44
55 33
22 44
40 22
13 31
42 22 40
44 55
51 42
23 33
43 23
24 22
60 51
22 31
66 44 24
14 34
40 22
21 23
75 66
45 55
66 44 24 22
11 33
42 24
35 13
57 35
25 45
51 40
13 22
52 42
```

- Improve the behavior of the tier 0 bot players.

- The description of the website is that of mecatronics on google.

- Repeated nav bar on top and side.

- Chat from the original metronics theme is showing.(to be deleted)
