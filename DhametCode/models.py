from django.db import models
from jsonfield import JSONField
import random
import string

def generate_game_code():
    length = 8
    while(True):
        Code = ''.join(random.choices(string.ascii_uppercase,k=length))
        if Game.objects.filter(Code=Code).count()==0:
            return Code
def get_initial_game_state():
    initial_game_state = {
      'board' : 
      [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
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
class Player(models.Model):
    Name = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images',null=True)
    Email = models.EmailField(null=True)
    Elo = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.Name}'

class Game(models.Model):

    Code = models.CharField(max_length=10,default=generate_game_code,blank=True,null=True)
    DateTime = models.DateTimeField(auto_now_add=True)
    # Players = models.ManyToManyField(Player,null=False)
    State = JSONField(default = get_initial_game_state) # the game state.
    player1 = models.CharField(max_length=200)
    player2 = models.CharField(max_length=200)
    Current = models.IntegerField(default=0) #who's Turn Right Now
    Length = models.IntegerField(default=0)
    Moves = models.TextField(max_length=10000,default="") # contain the moves of the game
    last_move = models.TextField(default="",null=True)
    Ongoing = models.BooleanField(default=False)
    Winner = models.IntegerField(blank=True,null=True)
   
    def __str__(self):
        # return f"{self.Players[0].Name} VS {self.Players[1].Name}"
        return f"{self.Code} created_at {self.DateTime}"

  


