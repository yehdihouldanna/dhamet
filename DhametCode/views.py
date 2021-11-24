from django.shortcuts import render
from django.http import HttpResponse
from .models import Game 
from rest_framework import generics , status
from rest_framework.response import Response
from .serializers import GameSerializer , CreateGameSerializer , GameMoveSerializer
from .utils.Board import State
import numpy as np
import sys

from users.models import User

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
        # serializer = self.serializer_class(data=request.data)
        # Code_ = self.request.session.session_key
        if request.user.is_authenticated:
            user = User.objects.filter(name = request.user.name)[0]
        else : 
            try:
                user = User.objects.filter(name = "Guest")[0]
            except:
                user = User(name = "Guest",phone=000)
                user.save()
            
        # if serializer.is_valid(): # needs to be integrated somehow , but for now it causes problem since the id can't be passed blank.
        queryset_ = Game.get_available_games()
        if len(queryset_): # if game
            game = queryset_[0]
            game.opponent = user
            game.save()
            print(f"User : {user.username} Have Joined the game {game.get_game_code()} created by {game.creator}")
            return Response(CreateGameSerializer(game).data,status = status.HTTP_202_ACCEPTED)
        else:

            game = Game(creator = user )
            game.save()
            print(f"User : {user.username} Have Created a game who's id is {game.get_game_code()}")
            return Response(CreateGameSerializer(game).data,status = status.HTTP_201_CREATED)

        # return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class GameMoveView(generics.ListAPIView):
    """The view that process the player's moves sent by the client"""
    serializer_class = GameMoveSerializer
    queryset = Game.objects.all()

    def get_game_update(self,game,current_turn,move):
        length = game.Length
        board = self.deserialize(game.State)
        game_instance = State(n=9,board=board,player = current_turn, length=length)
        print('the move received is : ', move)
        # game_instance.show_board(file=sys.stderr)
        moves = move.split(" ")
        moved = False
        for k in range(len(moves)-1):
            source = moves[k]
            destination = moves[k+1]
            xs,ys = [int(i) for i in source]
            xd,yd = [int(i) for i in destination]
            # print(f"Moving form {xs}{ys} to {xd}{yd}")
            moved = game_instance.move((xs,ys),(xd,yd))
            if not moved:
                break
        if moved:
            ended  = game_instance.check_end_condition()
            game_instance.player = not game_instance.player
            game_instance.length+=1
            return True, game_instance.board,ended,game_instance.player,game_instance.length,game_instance.winner
        
        return False ,None,None,None,None,None

    def serialize(self,board):
        "serialize the matrix board into a string format"
        txt  =""
        for i in range(9):
            for j in range(9):
                if board[i,j]==1:
                    txt+="w"
                elif board[i,j]==3:
                    txt+="W"
                elif board[i,j]==0:
                    txt+="_"
                elif board[i,j]==-1:
                    txt+="b"
                elif board[i,j]==-3:
                    txt+="B"

        return txt

    def deserialize(self,txt):
        "deserialize a string board into a matrix board"

        board = np.zeros((9,9),dtype=int)
        k = 0
        for i in range(9):
            for j in range(9):
                if txt[k]=="w":
                    board[i,j]=1
                elif txt[k]=="W":
                    board[i,j]=3
                elif txt[k]=="_":
                    board[i,j]=0
                elif txt[k]=="b":
                    board[i,j]=-1
                elif txt[k]=="B":
                    board[i,j]=-3
                k+=1
        return board

    def post(self,request,format=None):
        """The view's main method for returning a reponse to client requests"""
        if not self.request.session.exists(self.request.session.session_key): # check if the session exists
            self.request.session.create()
        serializer = self.serializer_class(data= request.data)

        if request.user.is_authenticated:
            user = User.objects.filter(name = request.user.name)
        else:
            user = User.objects.filter(name = "Guest")

        if serializer.is_valid():
            id = serializer.data.get('id')
            if id!="":
                queryset = Game.objects.filter(id=id)
                if queryset.exists():
                    current_turn  = serializer.data.get('current_turn')
                    board_txt =serializer.data.get('state')
                    move = serializer.data.get('last_move')
                    print(f"in the post method move:{move}")
                    game = queryset.filter(id=id)[0]
                    moved,board,ended,player,length,winner = self.get_game_update(game,current_turn,move)
                    if moved :
                        board_txt=self.serialize(board)
                        game.state = board_txt
                        game.length = length
                        moves = game.moves+"\n"+move
                        game.moves = moves
                        game.last_move = move

                        if ended:
                            game.winner = user
                        game.save()

                        # # if the player moved and we are playing vs an AI the AI moves too:
                        # if queryset[0].player1=="AI" and Current_Player==0 or queryset[0].player2 =="AI" and Current_Player==1:
                        #     agent = Player.
                        return Response(GameMoveSerializer(game).data,status = status.HTTP_202_ACCEPTED)
                
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

def say_hello(request):
    try :
        params = request.data
        return render(request,"index.html",{})
    except:
        return HttpResponse("Problem when accessing the game data")


def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', 
    {
        'room_name': room_name,
    })