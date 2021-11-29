""" this file contains the consumers for the web sockets which allows
for multiple players to connect to the same game.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils.Board import State
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

    def get_game_update(self,game,current_turn,move):
        length = game.length
        board = self.deserialize(game.state)
        game_instance = State(n=9,board=board,player = current_turn, length=length)
        # print('the move received is : ',move)
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
            return True, game_instance.board,ended,game_instance.length
        
        return False ,None,None,None

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

        moved = False
        if id!="":
            queryset = Game.objects.filter(id=id)
            if queryset.exists():
                # current_turn  = data['current_turn']
                board_txt = data['state']
                move = data['last_move']
                print(f"in the post method move:{move}")
                game = queryset[0]
                current_turn = game.current_turn
                print("first move : current turn is :",current_turn )
                moved,board,ended,length = self.get_game_update(game,current_turn,move)
                if moved :
                    board_txt = self.serialize(board)
                    game.state = board_txt
                    game.length = length
                    moves = game.moves+"\n"+move
                    game.moves = moves
                    game.last_move= move
                    game.current_turn = (game.current_turn+1)%2
                    
                    if ended:
                        game.winner= user
                        game.completed = datetime.now()

                    game.save()

                winner=""

                try:
                    winner = game.winner.name
                except:
                    pass

                output_data  = json.dumps({
                    'id':id,
                    'state': game.state,
                    'last_move': move,
                    'current_turn':game.current_turn,
                    'winner' : winner})
                
                return output_data
        
        raise Exception("You can't make a move in a non existing game!!")
        
        