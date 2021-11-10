from django.db import models
import random
import string

def generate_game_code():
    length = 8
    while(True):
        code = ''.join(random.choices(string.ascii_uppercase,k=length))
        if Game.objects.filter(code=code).count()==0:
            return code

# Create your models here.
class Player(models.Model):
    Name = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images')
    Email = models.EmailField()
    Elo = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.Name}'

class Game(models.Model):
    Code = models.CharField(max_length=10,default="",unique = True)
    DateTime = models.DateTimeField(auto_now_add=True)
    Players = models.ManyToManyField(Player,null=False)
    Current = models.IntegerField(default=0) #who's Turn Right Now
    Length = models.IntegerField(default=0)
    Moves = models.TextField(max_length=10000,default="") # contain the moves of the game
    Ongoing = models.BooleanField(default=False)
    Winner = models.IntegerField(blank=True,null=True)
   
    def __str__(self):
        # return f"{self.Players[0].Name} VS {self.Players[1].Name}"
        return f"{self.Code} created_at {self.DateTime}"



