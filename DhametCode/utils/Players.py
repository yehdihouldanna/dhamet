#------------------------------------------------
# Copyrigh (c) SMART Solutions SM SA® 2021.
# All rights reserved.
# Code made by : Yehdhih ANNA (TheLuckyMagician).
#------------------------------------------------

import numpy as np
import random
from termcolor import cprint

class Player():
    def __init__(self,name,player):
        self.name = name
        self.player= player # which color is the player's(0 for white and 1 for black)

    def move(self,state):
        pass

class Human(Player):
    def __init__(self,name,player):
        super().__init__(name,player)

    def move(self,state):
        move_ = input(f"{self.name} Enter your move : ")
        return move_

class Agent(Player):
    def __init__(self,name,player):
        super().__init__(name,player)
        self.pieces_indices=None

    def get_pieces(self,state):
        if self.player: #case the agent is playing with black pieces
            self.pieces_indices = np.argwhere(state.board<=-1)
        else :
            self.pieces_indices = np.argwhere(state.board>=1)

    def move(self,state):
        pass

class Naive(Agent):
    """
    This random agent will take the first available move
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Naive " + name

    def move(self,state):
        move="_"
        self.get_pieces(state)
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
        super().__init__(name,player)
        self.name = "Random " + name
        self.choices_limit = 5
    def move(self,state):
        move="_"
        dict_ = {}
        self.get_pieces(state)
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
    This is a dummy agent it choses the best move available to it in it's turn
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Dummy " + name
        self.choices_limit = 40 # could be limited if needed.
    def move(self,state):
        move="_"
        dict_ = {}
        self.get_pieces(state)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            chains = state.get_chain_moves(x,y)
            if len(chains):
                best_cp_move = max(chains, key=chains.get)
                score = chains[best_cp_move]
                dict_[best_cp_move] = score

            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            move  = max(dict_, key=dict_.get)
        return move

class MinMax(Agent):
    """
    This is a dummy agent it choses the best move available to it in it's turn
    """
    def __init__(self,name,player,depth = 2):
        super().__init__(name,player)
        self.name = "Dummy " + name
        self.choices_limit = 5
        self.depth = 2

    def move(self,state):
        score = 0
        cur_depth = 1
        maxi_turn = 1
        best_move,_ = self.minmax(state,score,cur_depth,self.depth,maxi_turn)
        if best_move is None:
            cprint(f"ALERT: {self.name} couldn't return a move!")
        return best_move

    # this is the strategy of the agent
    def minmax(self,state,score,cur_depth,target_depth,maxi_turn):
        if maxi_turn: # agent turn to maximize
            pieces = np.argwhere(state.board<=-1) if self.player else np.argwhere(state.board>=1)
        else: # agent adversary turn to minimize
            pieces = np.argwhere(state.board<=-1) if not self.player else np.argwhere(state.board>=1)
        if cur_depth==target_depth: # base scenario for recursivity
            best_move = None
            best_score = None
            for i in range(pieces.shape[0]):
                x,y = tuple(pieces[i])
                chains = state.get_chain_moves(x,y)
                if len(chains):
                    new_move = max(chains, key=chains.get)
                    new_score = chains[new_move]
                    if  best_score is None or new_score > best_score:
                        best_score = new_score
                        best_move = new_move

            if best_move is None:
                return "",score
            elif maxi_turn:
                return best_move, score + best_score
            else:
                return best_move, score - best_score

        else: # recursive call scenario
            temp_board = np.copy(state.board)
            player = state.player
            last_player = state.last_player
            best_move = None
            best_score = None
            for i in range(pieces.shape[0]):
                x,y = tuple(pieces[i])
                chains = state.get_chain_moves(x,y)
                # TODO : check for a way to make it possible to cover more exploration while looking for the best move
                if len(chains):
                    new_move = max(chains, key=chains.get)
                    new_score = chains[new_move]
                    score_ = (score + new_score) if maxi_turn else (score - new_score)
                    moved = state.move_from_str(new_move)
                    ended,_ = state.check_end_condition()
                    if not moved:
                        print(f"MinMax Agent tried the move: {new_move} but couldn't perform it!")
                    if not ended:
                        b1_move , b1_score = self.minmax(state,score_,cur_depth+1,target_depth,(maxi_turn+1)%2)
                        if best_score is None or b1_score > best_score :
                            best_score = b1_score
                            best_move = new_move
                    else:
                        if maxi_turn:
                            best_move = new_move
                            best_score = score_
                            break
                        elif best_score is None or score_>best_score:
                            best_move=new_move
                            best_score = score_

                    state.set_board(temp_board)
                    state.set_player(player)
                    state.set_last_player(last_player)
            return best_move,best_score
