""" this file contains the consumers for the web sockets which allows
for multiple players to connect to the same game.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils.Board import State
from .utils.Players import Random, Dummy , MinMax
from DhametCode.models import Game
from users.models import User
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import sys
from datetime import datetime

# This is a functional chat conumer could be used later to add a chat functionality.
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"room_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        tdj = text_data_json
        print("the received data is : ",text_data_json)
        message = str(self.user) +" says : "+ tdj['message']+"\n"
        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.user = self.scope['user']
        self.game_group_name = f"game_{self.game_code}"
        # Join game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # tdj = text_data_json
        print("the received data is : ",text_data_json)
        message = "from backend, " + str(self.user) + " moved."
        print(message)
        # Send message to game group
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'move_message',
                'data': text_data_json
            }
        )

    # Receive message from game group
    async def move_message(self, event):
        print("entering the move message method")
        # data = event['data']
        # sender = self.scope["user"].username
        # receiver = self.scope['path'].split('_')[1]
        output_data = await self.post_move(event)
        # Send message to WebSocket
        await self.send(text_data = output_data)

    def update_game(self,id,user,game,game_instance,move):
        moved = game_instance.move_from_str(move)
        if moved:
            game_instance.player = not game_instance.player
            game_instance.length+=1
            board_txt = self.serialize(game_instance.board)
            game.state = board_txt
            game.length = game_instance.length
            moves = game.moves+"\n"+move
            game.moves = moves
            game.last_move= move
            game.current_turn = (game.current_turn+1)%2
        ended,end_msg = game_instance.check_end_condition()
        if ended:
            game.winner = user
            game.completed = datetime.now()
        game.save()
        winner=""
        try:
            winner = game.winner.name
            if(not len(winner)):
                winner = game.winner.username
        except:
            pass
        output_data  = json.dumps({
                    'id':id,
                    'state': game.state,
                    'last_move': move,
                    'current_turn':game.current_turn,
                    'creator' : game.creator.name,
                    'opponent' : game.opponent.name,
                    'winner' : winner})
        return output_data


    def serialize(self,board):
        "serialize the matrix board into a string format"
        txt  =""
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
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
        n = int(np.sqrt(len(txt)))
        board = np.zeros((n,n),dtype=int)
        k = 0
        for i in range(n):
            for j in range(n):
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

    @database_sync_to_async
    def post_move(self , event):
        user = self.scope['user']
        data = event["data"]
        print(f"Starting the post_move method with sender : {user.username}\n data : {data}")
        id = data["id"]

        if user.is_authenticated:
            user = User.objects.filter(name = user.name)[0]
        else:
            user = User.objects.filter(name = "Guest")[0]

        if id!="":
            queryset = Game.objects.filter(id=id)
            if queryset.exists():
                current_turn_game  = data['current_turn']
                move = data['last_move']
                print(f"in the post method move:{move}")
                game = queryset[0]
                current_turn = game.current_turn
                length = game.length
                board = self.deserialize(game.state)
                game_instance = State(n=9,board=board,player = current_turn, length=length)
                
                AI_NAMES = ["AI_Random","AI_Dummy","AI_MinMax"]
                if ((game.creator==user and current_turn_game==0) or (game.opponent == user and current_turn_game)): # user is playing
                    return self.update_game(id,user,game,game_instance,move)
                
                elif ((game.opponent.name in AI_NAMES and current_turn_game) or (game.creator.name in AI_NAMES and current_turn_game==0)): # the AI is playing 
                    # Agent = Random('AI',current_turn)
                    # Agent = Dummy('AI',current_turn)
                    Agent = MinMax("AI",current_turn,depth=2)
                    move = Agent.move(game_instance)
                    print(f"The AI agent moved : {move}")
                    user_ = game.creator if game.creator.name in AI_NAMES else game.opponent
                    return self.update_game(id,user_,game,game_instance,move)

            # raise Exception(f"user {user.name} tried to make a non valid move!")    
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        # raise Exception("You can't make a move in a non existing game!!")
        
        