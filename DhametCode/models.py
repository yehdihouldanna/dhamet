from django.db import models
import random
import string
from users.models import User
import json
import time
from datetime import datetime
def generate_game_code():
    length = 8 # the code length curr
    chain_source = string.ascii_uppercase+string.ascii_lowercase+"0123456789" # chain containing the type of caracters to generate the code from
    # chain contains 26+26+10=52 ==>5.3*10^13 (possibilities)
    while(True):
        Code = ''.join(random.choices(chain_source,k=length))
        if Game.objects.filter(Code=Code).count()==0:
            return Code
def get_initial_state_json():
    initial_game_state = {
      'board' : [
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
      [ 1,  1,  1,  1,  0, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1],
      [-1, -1, -1, -1, -1, -1, -1, -1, -1,]]}

    return initial_game_state
# Create your models here.

class Game(models.Model):
    init_txt="wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbbb_wwwwbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    default_time = 5*60 # 10min in (s)
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank = True , null = True)
    modified = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(User, related_name = 'creator',on_delete=models.CASCADE)
    opponent = models.ForeignKey(User,related_name = 'opponent',null=True,blank=True,on_delete=models.CASCADE)
    winner = models.ForeignKey(User,related_name = "winner",blank =True,null=True,on_delete=models.CASCADE)

    creator_time = models.IntegerField(default=default_time)
    opponent_time = models.IntegerField(default=default_time, null = True,blank = True)

    state = models.CharField(max_length = 81, default = init_txt,blank=False,null=False)
    current_turn = models.IntegerField(default=0) # who's Turn Right Now (0:creator , 1 : opponent)
    last_move = models.CharField(max_length=100,default="",null=True)
    last_move_time = models.FloatField(default = time.time)
    length = models.IntegerField(default=0)

    moves = models.TextField(max_length=10000,default="") # contain the moves of the game

    def __str__(self):
        return f"{self.get_game_code()} created_at {self.created}"

    def get_creator_name(self):
        return self.creator.username
    def get_opponent_name(self):
        return self.opponent.username
    def get_winner_name(self):
        if self.winner:
            return self.winner.username
        else:
            return ""

    def get_game_code(self):
        return self.pk

    @staticmethod
    def get_available_games(user = None):
        if user is not None:
            return Game.objects.filter(creator = user , opponent =None,completed=None)
        return Game.objects.filter(opponent=None,completed = None)

    @staticmethod
    def created_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user) | Q(creator=user))

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass


    def update_users_scores(self):
        score_diff = self.creator.score - self.opponent.score
        f_1 = lambda x: min(int(3*x/100+8),25)  # A=(0,8), B=(400,20) caped at 25
        f_2 = lambda x: max(int(-3*x/200+8),1)  # A=(0,8), B=(400,2)  caped at 1
        if self.winner == self.creator :
            score_change = f_2(abs(score_diff)) if score_diff > 0 else f_1(abs(score_diff))
            self.creator.update_user_score(score_change)
            self.opponent.update_user_score(-score_change)
        elif self.winner ==self.opponent:
            score_change = f_1(abs(score_diff)) if score_diff >0 else f_2(abs(score_diff))
            self.opponent.update_user_score(score_change)
            self.creator.update_user_score(-score_change)


    def update_game(self,id,user,game_instance,move,souffle_move=""):
        if type(souffle_move)==str and souffle_move!="":
            game_instance.apply_souffle(souffle_move)
        if move =="":
            winner=""
            winner_score = ""
            try:
                winner = self.winner.username
                winner_score = self.winner.score
            except:
                pass
            opponent = ""
            opponent_score = ""
            try:
                opponent = self.opponent.username
                opponent_score = self.opponent.score
            except:
                pass
            tier = 0
            try:
                if self.opponent.is_fake:
                    tier = self.opponent.tier
            except:
                pass
            output_data  = json.dumps({
                        'id':id,
                        'state': self.state,
                        'last_move': self.last_move,
                        'current_turn':self.current_turn,
                        'creator' : self.creator.username,
                        'creator_score' : self.creator.score,
                        'opponent' : opponent,
                        'opponent_score' : opponent_score,
                        'soufflables' : [],
                        'winner' : winner,
                        'winner_score' : winner_score,
                        'tier' : tier,
                        })
        else:
            moved,soufflables = game_instance.move_from_str(move)
            if moved:
                game_instance.player = not game_instance.player
                game_instance.length+=1
                board_txt = game_instance.serialize(game_instance.board)
                self.state = board_txt
                self.length = game_instance.length
                moves = self.moves+"\n"+move
                self.moves = moves
                self.last_move= move
                self.current_turn = (self.current_turn+1)%2
            ended,end_msg = game_instance.check_end_condition()
            if ended:
                self.winner = user
                self.update_users_scores()
                self.completed = datetime.now()
            self.save()
            winner=""
            winner_score=""
            try:
                winner = self.winner.username
                winner_score = self.winner.score
            except:
                pass
            if self.opponent.is_fake:
                tier = self.opponent.tier
            else:
                tier=0
            output_data  = json.dumps({
                        'id':id,
                        'state': self.state,
                        'last_move': self.last_move,
                        'current_turn':self.current_turn,
                        'creator' : self.creator.username,
                        'opponent' : self.opponent.username,
                        'opponent_score' : self.opponent.score,
                        'tier' : tier,
                        'soufflables' : soufflables,
                        'winner' : winner,
                        'winner_score' : winner_score,
                        'winner' : winner
                        })
        return output_data

    def update_timers(self,current_user):
        """updates front-end timers based on the ground truth back-end ones"""
        if not self.completed:
            current_time = time.time()
            time_diff = current_time-self.last_move_time
            time_diff_sec = int(time_diff)
            if current_user == 0:
                if self.creator_time<=0.3:
                    self.winner = self.opponent
                    self.update_users_scores()
                    self.completed = datetime.now()
                self.creator_time -= time_diff_sec
            elif current_user == 1:
                if self.opponent_time <= 0.3:
                    self.winner = self.creator
                    self.update_users_scores()
                    self.completed= datetime.now()
                self.opponent_time -= time_diff_sec
            self.last_move_time = time.time()
            self.save()

    def timer_request_response(self):
        output_data  = json.dumps({
                        'id':self.get_game_code(),
                        'type':"timer",
                        'current_turn': self.current_turn,
                        'creator_time' : self.creator_time,
                        'opponent_time' : self.opponent_time,
                        'winner' : self.get_winner_name(),
                        })
        return output_data
