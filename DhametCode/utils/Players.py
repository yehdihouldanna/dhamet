#------------------------------------------------
# Copyrigh (c) SMART Solutions SM SA® 2021.
# All rights reserved.
# Code made by : Yehdhih ANNA (TheLuckyMagician).
#------------------------------------------------

import numpy as np
import random

class Player():
    def __init__(self,name,player):
        self.name = name
        self.player= player # which color is the player's(0 for white and 1 for black)

    def move(self,state):
        pass

class Human(Player):
    def __init__(self,name,player):
        self.name = name
        self.player = player

    def move(self,state):
        move_ = input(f"{self.name} Enter your move : ")
        return move_

class Agent(Player):
    def __init__(self,name,player):
        self.name = name
        self.player = player

    def move(self,state):
        pass

class Naive(Agent):
    """
    This random agent will take the first available move
    """
    def __init__(self,name,player):
        self.name = "Naive " + name
        self.player  = player
        self.pieces_indices=None
    def move(self,state):
        move="_"
        if self.player: #case the agent is playing with black pieces
            self.pieces_indices = np.argwhere(state.board<=-1)
        else :
            self.pieces_indices = np.argwhere(state.board>=1)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            moves,scores = state.available_moves(x,y)
            if len(moves):
                movet = moves[0]
                move = str(x)+str(y)+" "+str(movet[0])+str(movet[1])
                print(self.name," moved : ",move)
                break
        return move

class Random(Agent):
    """
    This a random agent that chooses a random move from the first available moves.
    """
    def __init__(self,name,player):
        self.name = "Random " + name
        self.player  = player
        self.pieces_indices=None
        self.choices_limit = 5
    def move(self,state):
        move="_"
        dict_ = {}
        if self.player: #case the agent is playing with black pieces
            self.pieces_indices = np.argwhere(state.board<=-1)
        else :
            self.pieces_indices = np.argwhere(state.board>=1)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            moves,scores= state.available_moves(x,y)
            if len(moves):
                source = str(x)+str(y)
                dict_[source]=moves
            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            key  = random.choice(list(dict_))
            destination = random.choice(dict_[key])
            move = key +" "+ str(destination[0])+str(destination[1])
        return move

class Dummy(Agent):
    """
    This is a dummy agent it choses the best move available to it in his turn
    """
    def __init__(self,name,player):
        self.name = "Dummy " + name
        self.player  = player
        self.pieces_indices=None
        self.choices_limit = 5
    def move(self,state):
        move="_"
        dict_ = {}
        if self.player: #case the agent is playing with black pieces
            self.pieces_indices = np.argwhere(state.board<=-1)
        else :
            self.pieces_indices = np.argwhere(state.board>=1)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            
            chains = state.get_chain_moves(x,y)
            if len(chains):
                best_cp_move = max(chains, key=chains.get)
                score = chains[best_cp_move]
                dict_[best_cp_move] = score
            else :    
                moves,_ = state.available_moves(x,y)
                # take one move randomly from the availble non take
                if len(moves):
                    move_ = random.choice(moves)
                    dict_[str(x)+str(y)+" "+str(move_[0])+str(move_[1])] = 0

            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            move  = max(dict_, key=dict_.get)
        return move


class BestOfFirst5(Agent):
    """
    This agent chooses the best move available among the moves of the first 5 pieces it scans
    """
    def __init__(self,name,player):
        self.name = "Random " + name
        self.player  = player
        self.pieces_indices=None
        self.choices_limit = 5
    def move(self,state):
        move="_"
        dict_ = {}
        if self.player: #case the agent is playing with black pieces
            self.pieces_indices = np.argwhere(state.board<=-1)
        else :
            self.pieces_indices = np.argwhere(state.board>=1)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            moves,scores = state.available_moves(x,y)
            if len(moves):
                source = str(x)+str(y)
                
                dict_[source]=moves
            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            key  = random.choice(list(dict_))
            destination = random.choice(dict_[key])
            move = key +" "+ str(destination[0])+str(destination[1])
        return move
