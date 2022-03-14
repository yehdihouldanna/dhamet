#------------------------------------------------
# Copyrigh (c) SMART Solutions SM SA® 2021.
# All rights reserved.
# Code made by : Yehdhih ANNA (TheLuckyMagician).
#------------------------------------------------
import numpy as np
from termcolor import cprint
from .Players import *
# from Players import *
import time
import os
from copy import deepcopy

class State():
    """
    This class contains the state of the game at a give turn,
    the main content of this class is the baord vairable which contains
    """
    def __init__(self,n=9,board=None,player =0,length=0,souffle = False,forced_souffle=False):
        self.n = n
        self.length = length
        self.player = player   # who's turn : 0 for white 1 for black.
        self.pieces = self.n**2 // 2  # number of pieces of each player.
        self.white_score = self.pieces
        self.black_score = self.pieces
        self.game_score = 0
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

        self.forced_souffle = forced_souffle

    def deep_copy(self):
        return deepcopy(self)
    def reset_state(self,state_copy):
        self = deepcopy(state_copy)

    def get_pieces(self,player,start_i=None,start_j=None,spiral_center=True):
        """ returns the pieces in a spiral way starting from the attention location at start_x and start_y"""
        if spiral_center or (start_i is not None and start_j is not None):
            pieces = []
            if start_i is None or start_j is None:
                start_i = self.n//2
                start_j = self.n//2
            valid_index =  lambda i,j : -start_i<=i and i<=self.n-start_i and -start_j<=j and j<self.n-start_j
            i = 0
            j = 0
            di = 0
            dj = -1
            k=0
            while(k<self.n**2):
                if valid_index(i,j):
                    k+=1
                    if self.board[start_i+i,start_j+j]<=-1 and player:
                        pieces.append([start_i+i,start_j+j])
                    elif self.board[start_i+i,start_j+j]>=1 and not player:
                        pieces.append([start_i+i,start_j+j])

                if i == j or (i < 0 and i == -j) or (i > 0 and i == 1-j):
                    di, dj = -dj, di
                i, j = i+di, j+dj
            return np.asarray(pieces)
        
        return np.argwhere(self.board<=-1) if player else np.argwhere(self.board>=1)

    def check_end_condition(self):
        if not self.player_has_moves():
            self.winner =["White" ,"Black"][not self.player]
            end_msg = f"{self.winner} Won! The adversary had no moves"
            return True,end_msg
        
        #TODO : add a game draw condition that doesn't cause the game to halt
        # elif self.no_kill_counter >=self.no_kill_limit:
        #     self.winner = "Draw"
        #     end_msg = "Game Draw!, by the long no killing moves!"
        #     return True,end_msg
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
            moves= self.available_moves(x,y)
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

    def format_move(self,move):
        new_text = ""
        alph = "ABCDEFGHI"
        if type(move)==str and len(move):
            new_text = " ".join([alph[int(x[1])]+str(int(x[0])+1) for x in move.split(" ")])
        return new_text

    def set_last_move(self,last_move):
        self.last_move = last_move

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
            max_score = max(possible_moves.values()) # aids in finding souvlables
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

            self.last_move_nature = score
    
            self.last_player = self.player

            return True,max_score

    def move_from_str(self,souffle_move,move_str):
        previous_board = np.copy(self.board)
        moves = move_str.split(" ")
        moved = False
        last_moved = None
        last_score = None
        if type(souffle_move)==str and souffle_move!="" :
            self.apply_souffle(souffle_move)
        for k in range(len(moves)-1):
            source = moves[k]
            destination = moves[k+1]
            xs,ys = [int(i) for i in source]
            xd,yd = [int(i) for i in destination]
            moved,last_score = self.move((xs,ys),(xd,yd))
            last_moved = (xd,yd)
            if not moved:
                break
        if moved and self.souffle:
            last_move_score = len(moves)-2+self.last_move_nature       
            self.update_soufflables(moves,previous_board,last_move_score)
        if not moved:
            self.board = previous_board # in case the souffle move messed up the current board
        return moved , self.soufflables

    def update_soufflables(self,moves_in,previous_board,last_move_score):
        aux = np.copy(self.board)  
        self.board = np.copy(previous_board) # you need the previous board for the soufflables elsewise it will be applied based on current board.
        self.soufflables = []
        pieces = self.get_pieces(self.player)
        max_score = 0
        current_score = 0
        for piece in pieces:
            if self.forced_souffle:
                chained_moves = self.get_chain_moves(piece[0],piece[1])
                if len(chained_moves):
                    current_score = max(chained_moves.values())
                    if (last_move_score < current_score) and (max_score<=current_score):
                        max_score = current_score
                        if max_score == current_score:
                            self.soufflables += [k[:2] for k,v in chained_moves.items() if (v == current_score and k[:2] not in self.soufflables)]
                        else:
                            self.soufflables  = [k[:2] for k,v in chained_moves.items() if (v == current_score and k[:2] not in self.soufflables)]
            else :
                moves = self.available_moves(piece[0],piece[1],lazy = True)
                if len(moves):
                    self.soufflables.append(str(piece[0])+str(piece[1]))

        from_ = moves_in[0]
        to_= moves_in[-1]
        if from_ in self.soufflables:
            self.soufflables.append(to_)
            self.soufflables.remove(from_)
        self.soufflables = list(set(self.soufflables))
        # if len(self.soufflables):
        #     cprint(f"the possible soufflables are : {[self.format_move(x) for x in self.soufflables]}", color = "green",attrs=["bold"])
        self.board = np.copy(aux)

    def apply_souffle(self,piece_str):
        if piece_str=="":
            return True
        if ((self.player and self.board[int(piece_str[0]),int(piece_str[1])]>=1) or (not self.player and self.board[int(piece_str[0]),int(piece_str[1])]<=-1)):
            self.board[int(piece_str[0]),int(piece_str[1])]=0
            self.can_souffle = False
            return True
        return False

    def get_best_chain_moves(self,pieces):
        """Loops over all the pices to get the best moves and the respective max score"""
        max_score = 0
        best_moves = []
        for x,y in pieces :
            chains = self.get_chain_moves(x,y)
            if len(chains):
                piece_score = max(chains.values())
                moves = [key for key,value in chains.items() if value == piece_score] # returns a set
                if max_score < piece_score:
                    if len(moves):
                        best_moves = moves
                        max_score = piece_score
                elif max_score == piece_score:
                    best_moves = best_moves+moves
        return best_moves,max_score


    def get_chain_moves(self,x,y):
        # TODO : optimize this function to return only the optimal chained move and reduce the overhead (apply some algorithm pruning principles )
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
        # if len(move_str)>=3*self.lim_takes+2: # just an overhead reducer could be made false in __init__
        #     return
        # else:
        attributes = self.get_attributes()
        possible_moves = self.available_moves(x,y)
        for (x_,y_) in possible_moves.keys():
            score = possible_moves[(x_,y_)]
            if score :
                move = move_str + " " +str(x_)+str(y_)
                chains[move] = chains[move_str] + 1
                self.move((x,y),(x_,y_))
                self.helper_chain_moves(x_,y_,move,chains,False)
                self.set_attributes(attributes)
            elif first_lvl and not score:
                move = move_str + " " +str(x_)+str(y_)
                chains[move] = 0

        
    def available_moves(self,x,y,lazy=False):
        """
        This function return all the available moves of the given piece, note that it contains all the logic of how the game pieces moves and such
        (it returns only one step and not like chained moves).
        params : x,y : piece coordinates on the board
                lazy : is boolean , if true it will return after the first occurance of score changing move.

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
        if type(board) == str :
            board = self.deserialize(board)
        assert board.shape == (self.n,self.n)
        self.board = np.copy(board)

    def set_player(self,player):
        if (type(player)==int and player==1) or (type(player)==str and player.lower()[0]=="b"):
                self.player = 1
        elif (type(player)==int and player==0) or (type(player)==str and player.lower()[0]=="w"):
                self.player = 0
        else:
            print("Trying to set an Invalid Player! : type '0' for 'White' or '1' for 'Black'")

    def set_attributes(self,n,length,player,pieces_count,
                        white_score,black_score,game_score_,
                        winner,souffle_allowed,can_souffle,soufflables,
                        last_move_nature,last_player,lim_takes,
                        board,forced_souffle):
        self.n = n
        self.length = length
        self.player = player  
        self.pieces = pieces_count
        self.white_score = white_score 
        self.black_score = black_score 
        self.game_score = game_score_
        # self.dhaimat_value = 3
        self.winner = winner  
        self.souffle = souffle_allowed 
        self.can_souffle = can_souffle
        self.soufflables = soufflables
        self.last_move_nature = last_move_nature 
        self.last_player = last_player
        self.lim_takes = lim_takes
        self.board = np.copy(board)
        self.forced_souffle = forced_souffle
    
    def set_attributes(self,attributes):
        self.n = attributes["n"]
        self.length = attributes["length"]
        self.player = attributes["player"]  
        self.pieces = attributes["pieces_count"]
        self.white_score = attributes["white_score"] 
        self.black_score = attributes["black_score"] 
        self.game_score = attributes["game_score_"]
        # self.dhaimat_value = attributes["3"]
        self.winner = attributes["winner"]  
        self.souffle = attributes["souffle_allowed"] 
        self.can_souffle = attributes["can_souffle"]
        self.soufflables = attributes["soufflables"]
        self.last_move_nature = attributes["last_move_nature"] 
        self.last_player = attributes["last_player"]
        self.lim_takes = attributes["lim_takes"]
        self.board = np.copy(attributes["board"])
        self.forced_souffle = attributes["forced_souffle"]

    def get_attributes(self):
        attributes = {
            "n":self.n,
            "length": self.length ,
            "player" : self.player ,  
            "pieces_count" :self.pieces ,
            "white_score":self.white_score , 
            "black_score":self.black_score , 
            "game_score_":self.game_score ,
            # self.dhaimat_value ,
            "winner": self.winner ,  
            "souffle_allowed" : self.souffle , 
            "can_souffle":self.can_souffle ,
            "soufflables" :self.soufflables ,
            "last_move_nature" : self.last_move_nature , 
            "last_player":self.last_player ,
            "lim_takes":self.lim_takes ,
            "board":np.copy(self.board) ,
            "forced_souffle": self.forced_souffle ,
        }
        return attributes

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
        move_str ,souffle_move = self.players[self.game.player].move(self.game,self.game.soufflables)
        print(f"Player {self.players[self.game.player]} is playing move : {move_str},souffle : {souffle_move}")
        moved,_= self.game.move_from_str(souffle_move,move_str)
        if moved:
            if self.console:
                self.game.show_board()
                self.game.show_score()

            self.game_ended,end_msg = self.game.check_end_condition()
            if self.game_ended :
                print(end_msg)
            if self.filepath :
                with open(self.filepath,mode="a") as f:
                    f.write(move_str+"\n")
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
