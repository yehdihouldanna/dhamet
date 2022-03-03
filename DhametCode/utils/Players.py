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

    def move(self,state,soufflables=[]):
        pass

class Human(Player):
    def __init__(self,name,player):
        super().__init__(name,player)

    def move(self,state,soufflables=[]):
        move_ = input(f"{self.name} Enter your move : ")
        return move_

class Agent(Player):
    def __init__(self,name,player):
        super().__init__(name,player)
        self.pieces_indices=None
    def move(self,state,soufflables=[]):
        pass

    def souffle(self):
        pass

class Naive(Agent):
    """
    This random agent will take the first available move
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Naive " + name

    def move(self,state,soufflables=[]):
        move=None
        state.get_pieces(self.player)
        for i in range(self.pieces_indices.shape[0]):
            x,y = tuple(self.pieces_indices[i])
            moves,scores = state.available_moves(x,y)
            if len(moves):
                movet = moves[0]
                move = str(x)+str(y)+" "+str(movet[0])+str(movet[1])
                print(self.name," moved : ",move)
                break
        if not move:
            cprint(f"ALERT: {self.name} couldn't return a move!",color = "red")
        return move

class Random(Agent):
    """
    This a random agent that chooses a random move from the first available moves.
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Random " + name
        self.choices_limit = 5
    def move(self,state,soufflables=[]):
        move=None
        dict_ = {}
        pieces = state.get_pieces(self.player)
        for i in range(pieces.shape[0]):
            x,y = tuple(pieces[i])
            possible_moves= state.available_moves(x,y)
            moves = list(possible_moves.keys())
            scores = possible_moves.values()
            if len(moves):
                source = str(x)+str(y)
                dict_[source]=moves
            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            key  = random.choice(list(dict_))
            destination = random.choice(dict_[key])
            move = key +" "+ str(destination[0])+str(destination[1])
        if not move:
            cprint(f"ALERT: {self.name} couldn't return a move!",color = "red")
        return move
class Random_plus(Agent):
    """
    This a random agent that chooses a random move from the first available moves.
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Random " + name
        self.choices_limit = 25
    def move(self,state,soufflables=[]):
        #TODO : The human-ish behavior of this IA could be improved by favoring horizontal and vertical moves over diagonal ones.
        move = None
        dict_ = {}
        scores = {}
        pieces = state.get_pieces(self.player)
        for i in range(pieces.shape[0]):
            x,y = tuple(pieces[i])
            possible_moves = state.available_moves(x,y)
            possible_moves = sorted(possible_moves.items(),key=lambda item:item[1],reverse=True)
            if len(possible_moves):
                source = str(x)+str(y)
                dict_[source]= possible_moves[0][0]
                scores[source] = possible_moves[0][1]
            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            gscores = dict([item for item in scores.items() if item[1]==1])
            if len(gscores): # to prefer more natural moves
                key = random.choice(list(gscores))
            else:
                key  = random.choice(list(dict_))
            # destination = random.choice(dict_[key])
            destination = dict_[key]
            move = key +" "+ str(destination[0])+str(destination[1])
        if not move:
            cprint(f"ALERT: {self.name} couldn't return a move!",color = "red")
        return move

class Dummy(Agent):
    """
    This is a dummy agent it choses the best move available to it in it's turn
    """
    def __init__(self,name,player):
        super().__init__(name,player)
        self.name = "Dummy " + name
        self.choices_limit = 40 # could be limited if needed.
    def move(self,state,soufflables=[]):
        move=None
        dict_ = {}
        pieces=state.get_pieces(self.player)
        for i in range(pieces.shape[0]):
            x,y = tuple(pieces[i])
            chains = state.get_chain_moves(x,y)
            if len(chains):
                best_cp_move = max(chains, key=chains.get)
                score = chains[best_cp_move]
                dict_[best_cp_move] = score

            if len(dict_)>= self.choices_limit:
                break
        if(len(dict_)):
            move  = max(dict_, key=dict_.get)
        if move =="_":
                cprint(f"ALERT: {self.name} couldn't return a move!",color = "red")
        return move

class MinMax(Agent):
    """
    This is a dummy agent it choses the best move available to it in it's turn
    """
    def __init__(self,name,player,depth = 2,allow_souffle=False):
        super().__init__(name,player)
        self.name = "Dummy " + name
        self.choices_limit = 5
        self.depth = 3

    def move(self,state,soufflables=[]):
        score = 0
        cur_depth = 1
        maxi_turn = 1
        if len(soufflables) : 
            souffle_move = soufflables[0]
            if  type(souffle_move)==str and souffle_move!="":
                state.apply_souffle(souffle_move)
        best_move,_ = self.minmax(state,score,cur_depth,self.depth,maxi_turn,soufflables)
        # if best_move is None:
        #     cprint(f"ALERT: {self.name} couldn't return a move!",color="red")
        return best_move

    # this is the strategy of the agent
    def minmax(self,state,score,cur_depth,target_depth,maxi_turn,soufflables):
        pieces = state.get_pieces(self.player) if maxi_turn else state.get_pieces(not self.player) # if maxi_turn we maximise for player, else we maximise for adversary
        
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

            #TODO : Causes the game to end before it's time, due to limited moves draw condition.
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
                
                if len(chains):
                    new_move = max(chains, key=chains.get)
                    new_score = chains[new_move]
                    score_ = (score + new_score) if maxi_turn else (score - new_score)
                    souffle_move = ""
                    if len(soufflables):
                        souffle_move = soufflables[0]

                    moved,soufflables = state.move_from_str(souffle_move,new_move)
                    ended,_ = state.check_end_condition()
                    if not moved:
                        print(f"MinMax Agent tried the move: {new_move} but couldn't perform it!")
                    if not ended:
                        b1_move , b1_score = self.minmax(state,score_,cur_depth+1,target_depth,(maxi_turn+1)%2,soufflables)
                        if best_score is None or b1_score > best_score :
                            best_score = b1_score
                            best_move = new_move
                    else:
                        if maxi_turn:
                            best_move  = new_move
                            best_score = score_
                            break
                        elif best_score is None or score_>best_score:
                            best_move=new_move
                            best_score = score_

                    state.set_board(temp_board)
                    state.set_player(player)
                    state.set_last_player(last_player)
            return best_move,best_score
