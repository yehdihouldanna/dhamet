from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.serializers import Serializer
from .models import Game ,Player
from rest_framework import generics , status
from rest_framework.response import Response
from .serializers import GameSerializer , CreateGameSerializer , GameMoveSerializer
from .utils.Board import State
# from .utils.Players import Human, Agent
# Create your views here.

class GameView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class CreateGameView(generics.ListAPIView):
    serializer_class = CreateGameSerializer  # a view requires a serializer_class and a queryset attributes
    queryset = Game.objects.all()

    def post(self,request,format = None):
        if not self.request.session.exists(self.request.session.session_key): # check if the session exists
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        Code_ = self.request.session.session_key
        print("-------------------------------------------------")
        print(serializer.is_valid())
        print("-------------------------------------------------")
        print(Code_,serializer.is_valid())
        if serializer.is_valid():
            player1 = serializer.data.get('player1')
            player2 = serializer.data.get('player2')
            game = Game(Code = Code_,player1=player1,player2=player2)
            game.save()
            return Response(CreateGameSerializer(game).data,status = status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class GameMoveView(generics.ListAPIView):
    serializer_class = GameMoveSerializer
    queryset = Game.objects.all()

    def get_game_update(game,Player,Move):
        length = game.length
        player = Player==game.player1
        if length %2 ==player:
            board = game.State.board
            game_instance = State(n=9,board=board,length=length)

            moves = Move.split(" ")
            moved = False
            for k in range(len(moves)-1):
                source = moves[k]
                destination = moves[k+1]
                xs,ys = [int(i) for i in source]
                xd,yd = [int(i) for i in destination]
                moved = game_instance.move((xs,ys),(xd,yd))
                if not moved:
                    break
            
            if moved:
                ended  = game_instance.check_end_condition()
                game_instance.player = not game_instance.player
                game_instance.length+=1
                return True, game_instance.board,ended,game_instance.player,game_instance.length,game_instance.winner
        
        return False ,None,None,None,None,None

    def post(self,request,format=None):
        serializer = self.serializer_class(data= request.data)
        
        if serializer.is_valid():
            # Code = self.request.session.session_key
            Code = serializer.data.get('Code')
            if Code!="":
                queryset = Game.objects.filter(Code=Code)
                if queryset.exists():
                    Player  = serializer.data.get('Player')
                    Move = serializer.data.get('last_move')
                    game = queryset.filter(Code=Code)[0]
                    moved,board,ended,player,length,winner = self.get_game_update(game,Player,Move)
                    if moved :
                        new_state={'board':board}
                        game.update(State=new_state)
                        game.update(Length=length)
                        Moves = game.Moves+"\n"+Move
                        game.update(Moves = Moves)
                        game.update(Ongoing=not ended)
                        if ended:
                            game.update(Winner= winner)
                        return Response(GameSerializer(game).data,status = status.HTTP_202_ACCEPTED)
                
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


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
