from django.db import models
import random
import string
from users.models import User
import json
import time
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
    default_time = 10*60 # 10min in (s)
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

    def update_timers(self,current_user):
        """updates front-end timers based on the ground truth back-end ones"""
        current_time = time.time()
        time_diff = current_time-self.last_move_time
        time_diff_sec = int(time_diff)
        if current_user ==0:
            self.creator_time-=time_diff_sec
            if self.creator_time==0:
                self.winner == self.opponent
        elif current_user == 1:
            self.opponent_time -= time_diff_sec
            if self.opponent_time == 0:
                self.winner == self.creator
        self.last_move_time = current_time
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
