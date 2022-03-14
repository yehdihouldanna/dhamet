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
        souffle = input(f"{self.name} Enter your soufflé : ")
        return move_,souffle

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
        souffle_move = ""
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
        return move,souffle_move

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
        souffle_move = ""
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
        return move,souffle_move
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
        souffle_move=""
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
        return move,souffle_move

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
        souffle_move = ""
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
        return move,souffle_move

class MinMax(Agent):
    """
    This is a dummy agent it choses the best move available to it in it's turn
    """
    def __init__(self,name,player,depth = 2,allow_souffle=False):
        super().__init__(name,player)
        self.name = "Dummy " + name
        self.choices_limit = 5
        self.depth = 3 # for better performance take a pair depth
                       # for testing reasons we need this to stay this way. for the long term run .
    def move(self,state,soufflables=[]):
        score = 0
        cur_depth = 0
        maxi_turn = 1
        print("The AI is thinking :")
        # best_move,_,souffle_move = self.minmax(state,cur_depth,self.depth,maxi_turn,soufflables)
        best_move,souffle_move = self.minimax_wrapper(state,soufflables, self.depth, False)
        print()
        # if best_move is None:
        #     cprint(f"ALERT: {self.name} couldn't return a move!",color="red")
        if best_move is None or souffle_move is None:
            cprint(f"MinMax Agent chose the move: {state.format_move(best_move)} with the soufflé {state.format_move(souffle_move)}!",color="red",attrs=["bold"])
        else:
            print(f"MinMax Agent chose the move: {state.format_move(best_move)} with the soufflé {state.format_move(souffle_move)}!")
        return best_move , souffle_move

    def minimax(self,state,soufflables, depth,alpha,beta, maximizing_player):
        """Returns the best evaluation based on minimax algorithm improved with pruning"""
        pieces =  state.get_pieces(self.player) if not maximizing_player else state.get_pieces(not self.player)
        attributes = state.get_attributes()
        ended,_ = state.check_end_condition()
        if depth == 0 or ended:
            return state.compute_game_score()
        if maximizing_player :
            max_eval = - 60
            for souffle in soufflables +  [""]:
                state.apply_souffle(souffle)  # applying souffle before searching for the moves
                moves,score = state.get_best_chain_moves(pieces) # getting all the possible best_moves
                for move in moves :
                    moved,soufflables_ = state.move_from_str(None,move)
                    eval = self.minimax(state,soufflables_,depth-1,alpha,beta,False)
                    max_eval = max(max_eval,eval)
                    alpha = max(alpha,eval)
                    state.set_attributes(attributes)
                    if beta <= alpha :
                        break
            return max_eval
        else:
            min_eval = + 60
            for souffle in soufflables +  [""]:
                state.apply_souffle(souffle)  # applying souffle before searching for the moves
                moves,score = state.get_best_chain_moves(pieces) # getting all the possible best_moves
                for move in moves :
                    moved,soufflables_ = state.move_from_str(None,move)
                    eval = self.minimax(state,soufflables_,depth-1,alpha,beta,True)
                    min_eval = min(min_eval, eval)  
                    beta = min(beta,eval)
                    state.set_attributes(attributes)  
                    if beta <=alpha :
                        break
            return min_eval

    def minimax_wrapper(self,state,soufflables, depth, maximizing_player):
        pieces =  state.get_pieces(self.player) if not maximizing_player else state.get_pieces(not self.player)
        best_move = None
        best_souffle = None
        best_move_score = None
        # alpha and beta for pruning.
        alpha_inf = -60
        beta_inf = 60
        attributes = state.get_attributes()
        for souffle in soufflables + [""]:
            state.apply_souffle(souffle)
            moves,score = state.get_best_chain_moves(pieces)
            for move in moves :
                moved,soufflables_ = state.move_from_str(None,move)
                eval_ = self.minimax(state,soufflables_, depth, alpha_inf,beta_inf, maximizing_player)
                if maximizing_player and (best_move_score is None or best_move_score < eval_):
                    best_move = move
                    best_souffle = souffle
                    best_move_score = eval_
                elif not maximizing_player and (best_move_score is None or best_move_score > eval_):
                    best_move = move
                    best_souffle = souffle
                    best_move_score = eval_
                state.set_attributes(attributes)
        return best_move , best_souffle
        

