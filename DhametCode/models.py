from django.db import models
import random
import string
from users.models import User

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
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank = True , null = True)
    modified = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(User, related_name = 'creator',on_delete=models.CASCADE)
    opponent = models.ForeignKey(User,related_name = 'opponent',null=True,blank=True,on_delete=models.CASCADE)
    winner = models.ForeignKey(User,related_name = "winner",blank =True,null=True,on_delete=models.CASCADE)

    state = models.CharField(max_length = 81, default = init_txt,blank=False,null=False)
    current_turn = models.IntegerField(default=0) # who's Turn Right Now (0:creator , 1 : opponent)
    last_move = models.CharField(max_length=100,default="",null=True)
    length = models.IntegerField(default=0)

    moves = models.TextField(max_length=10000,default="") # contain the moves of the game

    def __str__(self):
        return f"{self.get_game_code()} created_at {self.created}"

    def get_game_code(self):
        return self.pk
    @staticmethod
    def get_available_games():
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

