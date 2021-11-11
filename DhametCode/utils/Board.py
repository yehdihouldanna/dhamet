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
    def __init__(self,n=9,board=None,length=0):
        self.n = n
        self.player = 0 # who's turn : 0 for white 1 for black.
        self.length = length
        self.player = self.length%2  # since white always start,we can get player from length.
        self.pieces = self.n**2 //2  # number of pieces of each player.
        self.white_score = 40
        self.black_score = 40
        self.game_score = 0
        self.no_kill_counter = 0 # a counter that helps break the game 
                                 # in case of long non killing periods
        self.no_kill_limit = 20
        self.dhaimat_value = 3 
        self.winner = None  # -1 for black , 0 for draw and 1 for white

        self.auto_souvle=True  # if a pices have a killing move and it does non killing move it get's killed it self
        # initialising the board matrix
        if board:
            self.board = np.zeros((n,n),dtype=int)
            count = 0
            for i in range(self.n):
                for j in range(self.n):
                    if count < self.pieces:
                        self.board[i,j]=1
                    elif count==self.pieces:
                        self.board[i,j]=0
                    else:
                        self.board[i,j]=-1
                    count+=1
        else:
            self.board = board

    def check_end_condition(self):
        if self.player_has_no_moves_condition():
            self.winner =["White" ,"Black"][not self.player]
            print(f"{self.winner} Won! The adversary had no moves")
            return True
        elif self.no_kill_counter >=self.no_kill_limit:
            self.winner = "Draw"
            print("Game Draw!, by the long no killing moves!")
            return True
        elif self.white_score==0:
            print("Black Won!")
            self.winner = "Black"
            return True
        elif self.black_score==0:
            print("White Won!")
            self.winner = "White"
            return True
        return False

    def player_has_no_moves_condition(self):
        pieces_indices=None
        if self.player:
            pieces_indices = np.argwhere(self.board<=-1)
        else:
            pieces_indices = np.argwhere(self.board>=1)
        for i in range(pieces_indices.shape[0]):
            x,y = tuple(pieces_indices[i])
            moves,scores= self.available_moves(x,y)
            if len(moves):
                return False
        return True

    def show_board(self):
        """Shows the board in a colorful manner"""
        for i in range(self.n -1,-1,-1):
            cprint('{0:>3}'.format(f"[{i}]"),color = "yellow",end =" ")
            print("[",end="")
            for j in range(0,self.n):
                a = self.board[i,j]
                if np.sign(a)==-1:
                # print('{0:>3}'.format(self.board[i,j]),end =" ")
                    cprint('{0:>3}'.format(a),color = "red",end =" ")
                elif np.sign(a)==1:
                    cprint('{0:>3}'.format(a),color = "green",end =" ")
                else:
                    print('{0:>3}'.format(a),end =" ")
            print("]")
        print("     ",end=" ")
        for j in range(0,self.n):
            cprint('{0:>3}'.format(f"[{j}]"),color = "yellow",end=" ")
        print()
           
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
        possible_moves,scores = self.available_moves(piece[0],piece[1])
        # print(piece,"->",possible_moves,"\n",scores)
        if destination not in possible_moves:
            print("Move is invalid !, Try again")
            return False
        else:
            if np.sign(self.board[piece[0],piece[1]])==[1,-1][self.player]: # check if the current piece belongs to the current player,
                idx = possible_moves.index(destination)
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
                
                if self.auto_souvle and scores[idx] == 0 and 1 in scores: # souvle kills itself
                    self.board[destination[0],destination[1]]=0
                # updating the repeating end_condition.
                current_white_score = self.white_score
                current_black_score = self.black_score
                self.update_scores()
                if current_white_score==self.white_score and current_black_score==self.black_score:
                    self.no_kill_counter+=1
                else:
                    self.no_kill_counter=0

                return True
            else:
                print("This piece is not yours!,Try again!")
                return False

    # def get_chained_kills(self,x,y):
    #     """this function returns moves and a relative score to each move
    #      the score is the sum value of the killed pieces during that move.
    #     """
    #     Chains = {}
    #     current_chain = str(x)+str(y)
    #     current_score = 0
    #     def helper(self,x,y,current):
    #         moves,scores = self.available_moves(self,x,y)
    #         if len(scores) and sum(scores):
    #             for (mov,score) in zip(moves,scores):
    #                 if score==1:
    #                     current_chain+=str(mov[0])+str(mov[1])
    #                     Chains[current]
    #                     helper(self,mov[0],mov[1],current)

            
    #         current = 
    #         if first:
    #             moves,scores = self.available_moves(self,x,y)
    #             for (sc,mov) in zip(moves,scores):
    #                 if sc ==1:
    #                     next_chain_moves,next_chain_scores = self.available_moves(self,mov[0],mov[1])

    #         pass    


    def available_moves(self,x,y):
        """
        This function return all the available moves of the given piece.
        params : x,y : piece coordinates on the board
        returns : possible moves - list containing tuples of coordinates of possible moves
                  scores  - list the scores of the moves (aka the number of pieces that move killed)
        """
        possible_moves = []
        scores = []
        # we have two type of nodes : '+' (Plus) and '*' (Star)
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
                            possible_moves.append((x_(1),y_(1)))
                            scores.append(0)
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==-1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves.append((x_(2),y_(2)))
                            scores.append(1)

                    else : # White Dhaimat piece:
                        valid = False
                        k=1 # cell incrementer.
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==1: # if users piece blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0: # two adjacent pieces blocking the line.
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                possible_moves.append((x_(k),y_(k)))
                                scores.append(p)
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
                            possible_moves.append((x_(1),y_(1)))
                            scores.append(0)
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==-1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves.append((x_(2),y_(2)))
                            scores.append(1)  
                    else : # White Dhaimat piece:
                        valid = False
                        k=1 
                        p=0 # number of pieces already jumped
                        if valid_index(x_(k),y_(k)):
                            valid = True
                        while(valid):
                            if  np.sign(self.board[x_(k),y_(k)])==1: # if users piece blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0:
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                possible_moves.append((x_(k),y_(k)))
                                scores.append(p)
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
                            possible_moves.append((x_(1),y_(1)))
                            scores.append(0)
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves.append((x_(2),y_(2)))
                            scores.append(1)
                    else : # White Dhaimat piece:
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
                                possible_moves.append((x_(k),y_(k)))
                                scores.append(p)
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
                            if  np.sign(self.board[x_(k),y_(k)])==-1: # if user's piece blocking the line
                                break
                            elif valid_index(x_(k+1),y_(k+1)) and self.board[x_(k+1),y_(k+1)]!=0 and self.board[x_(k),y_(k)]!=0: # if two successif piecse are blocking the line
                                break
                            elif self.board[x_(k),y_(k)]==0: # a killing move
                                possible_moves.append((x_(k),y_(k)))
                                scores.append(p)
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
                            possible_moves.append((x_(1),y_(1)))
                            scores.append(0)
                        elif valid_index(x_(1),y_(1)) and np.sign(self.board[x_(1),y_(1)])==1 and valid_index(x_(2),y_(2)) and self.board[x_(2),y_(2)]==0:
                            possible_moves.append((x_(2),y_(2)))
                            scores.append(1)
                    else : # White Dhaimat piece:
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
                                possible_moves.append((x_(k),y_(k)))
                                scores.append(p)
                            elif np.sign(self.board[x_(k),y_(k)])==1: # enemy piece
                                p+=1
                            k+=1
                            valid = valid_index(x_(k),y_(k))
        return possible_moves,scores

    def update(self):
        pass

    def set_board(self,board):
        """this method sets the board to a given state
        mainly used for unit testing."""
        assert board.shape == (self.n,self.n)
        self.board = board

    def set_player(self,player):
        """this method sets the player manually , used for unit testing."""
        if player.lower() in ["b","black"] or player ==1:
                self.player = 1
        elif player.lower() in ["w" , "white"] or player==0:
                self.player = 0
        else:
            print("Trying to set an Invalid Player! : type '0' for 'White' or '1' for 'Black'")


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

            self.game_ended = self.game.check_end_condition()
            if self.filepath :
                with open(self.filepath,mode="a") as f:
                    f.write(move_+"\n")
            self.game.player = not self.game.player


if __name__=="__main__":
    # Player1 = Human("Saadna",0)
    # Player1 = Human("Aleyen",0)
    Player1 = Random("Agent 1",0)
    Player2 = Random("Agent 2",1)
    print("The game started :" )
    print(f"{Player1.name} is playing White.")
    print(f"{Player2.name} is playing Black.")
    name = "game" + str(time.time()) +".txt"
    file_name= os.path.join(os.getcwd(),"logs",name)
    match = Play_Game(Player1,Player2,n=9,file_name=file_name)
    while(not match.game_ended):
        match.turn()
    with open(os.path.join(os.getcwd(),"logs","labels.txt"),mode="a") as f:
        f.write(name+","+match.game.winner+"\n")