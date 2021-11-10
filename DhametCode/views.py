from django.shortcuts import render
from django.http import HttpResponse
from .models import Game ,Player
from rest_framework import generics
from .serializers import GameSerializer
# Create your views here.

class GameView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer



def say_hello(request):
    try :
        # we can pull data from a database
        # transform data
        game = Game.objects.all()
        print(game)
        # send email ...
        player = Player.objects.filter(Name="Yehdhih ANNA")[0];

        print(game)
        print(player)
        params = { 
                    "player1":game[0].Player1,
                    "player1_profile" : player.Image.url,
                    "player2":game[0].Player2,
                    'moves' : game[0].Moves
                }
        return render(request,"index.html",params)
    except:
        return HttpResponse("Problem when accessing the game data")
