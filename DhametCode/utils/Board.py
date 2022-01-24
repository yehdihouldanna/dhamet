#------------------------------------------------
# Copyrigh (c) SMART Solutions SM SA® 2021.
# All rights reserved.
# Code made by : Yehdhih ANNA (TheLuckyMagician).
#------------------------------------------------

import numpy as np
from termcolor import cprint
from .Players import *
import time
import os

class State():
    """
    This class contains the state of the game at a give turn,
    the main content of this class is the baord vairable which contains
    """
    def __init__(self,n=9,board=None,player =0,length=0,souffle = False):
        self.n = n
        self.length = length
        self.player = player   # who's turn : 0 for white 1 for black.
        self.pieces = self.n**2 // 2  # number of pieces of each player.
        self.white_score = self.pieces
        self.black_score = self.pieces
        self.game_score = 0
        self.no_kill_counter = 0 # a counter that helps break the game
                                 # in case of long non killing periods
        self.no_kill_limit = 20
        self.dhaimat_value = 3
        self.winner = None  # -1 for black , 0 for draw and 1 for white

        self.souffle = souffle  # سوفلة
        self.can_souffle = True
        self.soufflables = []


        self.last_move_nature = None # 0/1 if the last move took an adversary piece
        self.last_player = None # just checks for the last player, this is used in chained moves optimization


        # initialising the board matrix
        self.lim_takes = 10  # limits AI takes per turn (improves performance (when the baord contain few Dhaimat pieces))
        if board is None:
            self.board = np.zeros((n,n),dtype=int)
            middle = n//2
            self.board[:middle,:]=1 # first full rows
            self.board[middle,:middle]=-1 # left side of the middle row
            self.board[middle,middle]=0  # the central cell
            self.board[middle,middle+1:]=1
            self.board[middle+1:]=-1
        elif type(board)==str:
            self.board = self.deserialize(board)
        else:
            self.board = np.copy(board) # we need a deep copy here in order to avoid some problems

    def get_pieces(self,player):
        return np.argwhere(self.board<=-1) if player else np.argwhere(self.board>=1)

    def check_end_condition(self):
        if not self.player_has_moves():
            self.winner =["White" ,"Black"][not self.player]
            end_msg = f"{self.winner} Won! The adversary had no moves"
            return True,end_msg
        elif self.no_kill_counter >=self.no_kill_limit:
            self.winner = "Draw"
            end_msg = "Game Draw!, by the long no killing moves!"
            return True,end_msg
        elif self.white_score==0:
            end_msg = "Black Won!"
            self.winner = "Black"
            return True,end_msg
        elif self.black_score==0:
            end_msg = "White Won!"
            self.winner = "White"
            return True,end_msg
        return False,""

    def player_has_moves(self):
        pieces_indices=None
        if self.player:
            pieces_indices = np.argwhere(self.board<=-1)
        else:
            pieces_indices = np.argwhere(self.board>=1)
        for i in range(pieces_indices.shape[0]):
            x,y = tuple(pieces_indices[i])
            moves= self.available_moves(x,y) # //TODO : Very bad place to call this function, find a better way to check for the end
            if len(moves):
                return True
        return False

    def show_board(self,file=None):
        """Shows the board in a colorful manner"""
        for i in range(self.n -1,-1,-1):
            cprint('{0:>3}'.format(f"[{i}]"),color = "yellow",end =" ",file=file)
            print("[",end="")
            for j in range(0,self.n):
                a = self.board[i,j]
                if np.sign(a)==-1:
                    cprint('{0:>3}'.format(a),color = "red",end =" ",file=file)
                elif np.sign(a)==1:
                    cprint('{0:>3}'.format(a),color = "green",end =" ",file=file)
                else:
                    print('{0:>3}'.format(a),end =" ",file=file)
            print("]",file=file)
        print("     ",end=" ",file=file)
        for j in range(0,self.n):
            cprint('{0:>3}'.format(f"[{j}]"),color = "yellow",end=" ",file=file)
        print(file=file,flush=True)

    def show_score(self):
        cprint('Scores : ',color="yellow",end=" ")
        cprint(f'[white] :{self.white_score}',color = "green",end =" ")
        cprint(f'[black] :{self.black_score}',color = "red")

    def update_game_score(self):
        self.game_score = self.white_score - self.black_score

    def update_scores(self):
        self.white_score = np.sum(np.where(self.board>=1,self.board,0))
        self.black_score = -1*np.sum(np.where(self.board<=-1,self.board,0))

    def compute_game_score(self):
        return np.sum(self.board)

    def __str__(self) -> str:
        return str(self.board)
    def __repr__(self):
        return str(self.board) +"\n" + "Current Player : "+['White','Black'][self.player]

    def move(self,piece,destination):
        """moves a piece, given its position coordinates and it's destination coordinates"""
        possible_moves = self.available_moves(piece[0],piece[1])
        score = 0
        try:
            score = possible_moves[destination]
        except :
            pass
        if destination not in possible_moves.keys():
            # print("Move is invalid !, Try again")
            return False,None
        elif (self.last_player==self.player and self.last_move_nature==0):
            # print("Move is invalid !, Try again")
            return False,None
        elif (score==0 and self.last_player==self.player):
            # print("Move is invalid !, Try again")
            return False,None
        else:
            max_score = max(possible_moves.values())
            if np.abs(destination[0]-piece[0])>=2 or np.abs(destination[1]-piece[1])>=2:
                vec_x = np.sign(destination[0]-piece[0])
                vec_y = np.sign(destination[1]-piece[1])
                a= np.abs(destination[0]-piece[0])
                b= np.abs(destination[1]-piece[1])
                k_max = max(a,b)
                x_ = lambda k : piece[0]+k*vec_x # returns the next abscisse
                y_ = lambda k : piece[1]+k*vec_y # returns the next ordinate
                for k in range(1,k_max):
                    if self.board[x_(k),y_(k)]!=0:
                        self.board[x_(k),y_(k)]=0

            self.board[destination[0],destination[1]] = self.board[piece[0],piece[1]]
            self.board[piece[0],piece[1]] = 0

            # replace with the Dhamet condition
            if self.player and destination[0]==0:
                self.board[destination[0],destination[1]]=-1*self.dhaimat_value
            elif not self.player and destination[0]==self.n-1 :
                self.board[destination[0],destination[1]]=self.dhaimat_value

            if not score:
                self.no_kill_counter+=1
                self.last_move_nature=0
            else:
                self.no_kill_counter=0
                self.last_move_nature=1

            self.last_player = self.player

            return True,max_score

    def move_from_str(self,move_str):
        moves = move_str.split(" ")
        moved = False
        last_moved = None
        last_score = None
        for k in range(len(moves)-1):
            source = moves[k]
            destination = moves[k+1]
            xs,ys = [int(i) for i in source]
            xd,yd = [int(i) for i in destination]
            moved,last_score = self.move((xs,ys),(xd,yd))
            last_moved = (xd,yd)
            if not moved:
                break


        if moved and self.souffle and self.last_move_nature == 0:
            self.update_soufflables(last_moved, last_score)
        return moved , self.soufflables

    def update_soufflables(self,last_moved,last_score):
        # TODO : Make a lazy search algorithm for soufflable ->
        # TODO : ->(u dont have to loop over all availbles moves for a piece it is enough to find one that has a score of 1)

        self.soufflables = []
        pieces = self.get_pieces(self.player)
        for piece in pieces:
            moves = self.available_moves(piece[0],piece[1],lazy = True)
            if len(moves):
                self.soufflables.append(str(piece[0])+str(piece[1]))

    def apply_souffle(self,piece_str):
        # if (piece_str in self.soufflables) and ((not self.player and self.board[int(piece_str[0]),int(piece_str[1])]>=1) or (self.player and self.board[int(piece_str[0]),int(piece_str[1])]<=-1)):
        if ((self.player and self.board[int(piece_str[0]),int(piece_str[1])]>=1) or (not self.player and self.board[int(piece_str[0]),int(piece_str[1])]<=-1)):

            self.board[int(piece_str[0]),int(piece_str[1])]=0
            can_souffle = False
            # print(f'Souffle applied on the piece {piece_str}')
            return True
        return False

    def get_chain_moves(self,x,y):
        # TODO : optimize this function to return only the optimal chained move and reduce the overhead
        """This function returns all possible moves including the chained ones.
        """
        chains = {}
        move_str = str(x)+str(y)
        chains [move_str]=0
        first_lvl = True
        self.helper_chain_moves(x,y,move_str,chains,first_lvl)
        del chains[move_str]
        # cprint(f"Chains : {chains}" ,color ="blue")
        return chains

    def helper_chain_moves(self,x,y,move_str,chains,first_lvl=False):
        if len(move_str)>=3*self.lim_takes+2: # just an overhead reducer could be made false in __init__
            return
        else:
            temp_board = np.copy(self.board)
            current_player = self.player
            last_player = self.last_player
            possible_moves = self.available_moves(x,y)
            for (x_,y_) in possible_moves.keys():
                score = possible_moves[ (x_,y_)]
                if score :
                    move = move_str + " " +str(x_)+str(y_)
                    chains[move] = chains[move_str] + 1
                    self.move((x,y),(x_,y_))
                    self.helper_chain_moves(x_,y_,move,chains,False)
                    self.set_board(temp_board)
                    self.set_player(current_player)
                    self.set_last_player(last_player)
                elif first_lvl and not score:
                    move = move_str + " " +str(x_)+str(y_)
                    chains[move] = 0

    def available_moves(self,x,y,lazy=False):
        """
        This function return all the available moves of the given piece, (one step only doesn't return chained moves).
        params : x,y : piece coordinates on the board
                lazy : is boolean , if true it will just return the first killing moves

        returns : possible moves - dict containing tuples of coordinates of possible moves with their respective scores
        """
        possible_moves = {}
        vectors_up_star = [(1,-1),(1,0),(1,1)]
        vectors_down_star = [(-1,-1),(-1,0),(-1,1)]
        vectors_up_plus = [(1,0)]
        vectors_down_plus = [(-1,0)]
        vectors_side = [(0,-1),(0,1)]

        valid_index = lambda i,j : i>=0 and i<self.n and j>=0 and j<self.n
        if self.board[x,y]>=1: #  White piece
            if x%2 == y%2: # case of '*' nodes
                for vec in vectors_up_star + vectors_down_star + vectors_side:
                    x_ = lambda k : x+k*vec[0] # returns the next abscisse
                    y_ = lambda k : y+k*vec[1] # returns the next ordinate
                    if self.board[x,y]==1: # regular white piece
                        if  valid_index(x_(1),y_(1)) and self.board[x_(1),y_(1)]==0 and vec in vectors_up_star:
                            if not lazy:
                                possible_moves[(x_(1),y_(1))]=0
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==-1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves[(x_(2),y_(2))]=1
                            if lazy:
                                return possible_moves # we have an element

                    else : # White Dhaimat piece:
                        valid = False
                        k=1 # cell incrementer.
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==1: # if a user's piece is blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0: # two adjacent pieces blocking the line.
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                if p and lazy:
                                    possible_moves[(x_(k),y_(k))]=p
                                    return possible_moves
                                possible_moves[(x_(k),y_(k))]=p
                            elif np.sign(self.board[x_(k),y_(k)])==-1: # a piece is present in the cell but we still need to check the next cell case.
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))

            else: # case of '+' nodes
                for vec in vectors_up_plus + vectors_down_plus + vectors_side:
                    x_ = lambda k : x+k*vec[0]
                    y_ = lambda k : y+k*vec[1] # returns the next ordinate
                    if self.board[x,y]==1: # regular white piece
                        if  valid_index(x_(1),y_(1)) and self.board[x_(1),y_(1)]==0 and vec in vectors_up_plus:
                            if not lazy:
                                possible_moves[(x_(1),y_(1))]=0
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==-1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves[(x_(2),y_(2))]=1
                            if lazy :
                                return possible_moves
                    else : # White Dhaimat piece:
                        valid = False
                        k=1
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==1: # if a user's piece is blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0:
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                if p and lazy:
                                    possible_moves[(x_(k),y_(k))]=p
                                    return possible_moves
                                possible_moves[(x_(k),y_(k))]=p
                            elif np.sign(self.board[x_(k),y_(k)])==-1:
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))

        elif self.board[x,y]<=-1: # Black piece
            if x%2 == y%2: # case of '*' nodes
                for vec in vectors_down_star + vectors_up_star + vectors_side:
                    x_ = lambda k : x+k*vec[0]
                    y_ = lambda k : y+k*vec[1] # returns the next ordinate
                    if self.board[x,y]==-1: # regular balck piece
                        if  valid_index(x_(1),y_(1)) and self.board[x_(1),y_(1)]==0 and vec in vectors_down_star:
                            if not lazy:
                                possible_moves[(x_(1),y_(1))]=0
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves[(x_(2),y_(2))]=1
                            if lazy :
                                return possible_moves
                    else : # Black Dhaimat piece:
                        valid = False
                        k=1
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==-1: # if a user's is piece blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0:
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                if p and lazy:
                                    possible_moves[(x_(k),y_(k))]=p
                                    return possible_moves
                                possible_moves[(x_(k),y_(k))]=p
                            elif np.sign(self.board[x_(k),y_(k)])==1: # enemy piece
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))

                        valid = False
                        k=1
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==-1: # if a user's piece is blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0: # if two successif piecse are blocking the line
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                if p and lazy:
                                    possible_moves[(x_(k),y_(k))]=p
                                    return possible_moves
                                possible_moves[(x_(k),y_(k))]=p
                            elif np.sign(self.board[x_(k),y_(k)])==1: # enemy piece
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))
            else : # case of '+' nodes
                for vec in vectors_down_plus + vectors_up_plus + vectors_side:
                    x_ = lambda k : x+k*vec[0]
                    y_ = lambda k : y+k*vec[1]
                    if self.board[x,y]==-1: # regular black piece
                        if  valid_index(x_(1),y_(1)) and self.board[x_(1),y_(1)]==0 and vec in vectors_down_plus:
                            if not lazy:
                                possible_moves[(x_(1),y_(1))]=0
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves[(x_(2),y_(2))]=1
                            if lazy:
                                return possible_moves
                    else : # Black Dhaimat piece:
                        valid = False
                        k=1
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==-1: # if users piece blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0:
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                if p and lazy:
                                    possible_moves[(x_(k),y_(k))]=p
                                    return possible_moves
                                possible_moves[(x_(k),y_(k))]=p
                            elif np.sign(self.board[x_(k),y_(k)])==1: # enemy piece
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))
        return possible_moves

    def serialize(self,board):
        "serialize the matrix board into a string format"
        txt  =""
        for i in range(self.n):
            for j in range(self.n):
                if board[i,j]==1:
                    txt+="w"
                elif board[i,j]==3:
                    txt+="W"
                elif board[i,j]==0:
                    txt+="_"
                elif board[i,j]==-1:
                    txt+="b"
                elif board[i,j]==-3:
                    txt+="B"
        return txt

    def deserialize(self,txt):
        "deserialize a string board into a matrix board"
        board = np.zeros((self.n,self.n),dtype=int)
        k = 0
        for i in range(self.n):
            for j in range(self.n):
                if txt[k]=="w":
                    board[i,j]=1
                elif txt[k]=="W":
                    board[i,j]=3
                elif txt[k]=="_":
                    board[i,j]=0
                elif txt[k]=="b":
                    board[i,j]=-1
                elif txt[k]=="B":
                    board[i,j]=-3
                k+=1
        return board

    def set_board(self,board):
        """this method sets the board to a given state
        mainly used for unit testing."""
        if type(board) == str :
            board = self.deserialize(board)
        assert board.shape == (self.n,self.n)
        self.board = np.copy(board)

    def set_player(self,player):
        """this method sets the player manually"""
        if (type(player)==int and player==1) or (type(player)==str and player.lower() in ["b","black"]):
                self.player = 1
        elif (type(player)==int and player==0) or (type(player)==str and player.lower() in ["w" , "white"]):
                self.player = 0
        else:
            print("Trying to set an Invalid Player! : type '0' for 'White' or '1' for 'Black'")

    def set_last_player(self,last_player):
        self.last_player = last_player

class Play_Game():
    def __init__(self,player1,player2,n=9,file_name=None,console=False):
        self.game = State(n)
        self.players = [player1,player2]
        self.game.show_board()
        self.game_ended = False
        self.filepath = file_name
        self.console = console

    def turn(self):
        move_ = self.players[self.game.player].move(self.game)
        moves = move_.split(" ")
        moved = False
        for k in range(len(moves)-1):
            source = moves[k]
            destination = moves[k+1]
            xs,ys = [int(i) for i in source]
            xd,yd = [int(i) for i in destination]
            moved = self.game.move((xs,ys),(xd,yd))
            if not moved:
                break
        if moved:
            if self.console:
                self.game.show_board()
                self.game.show_score()

            self.game_ended,end_msg = self.game.check_end_condition()
            if self.game_ended :
                print(end_msg)
            if self.filepath :
                with open(self.filepath,mode="a") as f:
                    f.write(move_+"\n")
            self.game.player = not self.game.player

if __name__=="__main__":
    Player1 = Human("Yehdhih",0)
    # Player1 = Human("Nevisse",0)
    # Player1 = Human("Aleyen",0)
    # Player1 = Random("Agent 1",0)
    # Player2 = Random("Agent 2",1)
    Player2 = MinMax("Min 1 : ",1,depth = 2)
    print("The game started :" )

    print(f"{Player1.name} is playing White.")
    print(f"{Player2.name} is playing Black.")

    save_to_file  = False

    if save_to_file:
        name = "game" + str(time.time()) +".txt"
        file_name= os.path.join(os.getcwd(),"logs",name)
    else :
        file_name = None
    match = Play_Game(Player1,Player2,n=9,file_name=file_name,console=True)
    while(not match.game_ended):
        match.turn()

    if save_to_file:
        with open(os.path.join(os.getcwd(),"logs","labels.txt"),mode="a") as f:
            f.write(name+","+match.game.winner+"\n")
