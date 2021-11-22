""" this file contains the consumers for the web sockets which allows
for multiple players to connect to the same game.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils.Board import State
from DhametCode.models import Game,Player
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import sys

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
        moved, output_data = await self.post_move(event)
        # Send message to WebSocket

        await self.send(text_data = output_data)
        # await self.send(text_data = json.dumps({'data': data}))


    # @database_sync_to_async
    # def post_move(self , sender  , receiver ,data):
    #     sender = Player.objects.filter(username = sender)[0]
    #     receiver = Player.objects.filter(username = sender)[0]
    #     Game.objects.create(sender = sender , receiver = receiver , text =data)    


    def get_game_update(self,game,Player,Move):
        length = game.Length
        board = self.deserialize(game.State)
        game_instance = State(n=9,board=board,player = Player, length=length)
        print('the move received is : ',Move)
        game_instance.show_board(file=sys.stderr)
        moves = Move.split(" ")
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

    @database_sync_to_async
    def post_move(self , event):
        sender = self.scope["user"].username
        # receiver = self.scope['path'].split('_')[1]
        data = event["data"]
        print(f"Starting the post_move method with sender : {sender}\n data : {data}")
        Code = data["Code"]
        # 'Code':this.state.Code,
        # 'State': this.state.board_txt,
        # 'last_move': move_str,
        # 'Current_Player':this.state.player,
        moved = False
        if Code!="":
            queryset = Game.objects.filter(Code=Code)
            if queryset.exists():
                Current_Player  = data['Current_Player']
                board_txt = data['State']
                Move = data['last_move']
                print(f"in the post method move:{Move}")
                game = queryset[0]
                moved,board,ended,player,length,winner = self.get_game_update(game,Current_Player,Move)
                if moved :
                    board_txt=self.serialize(board)
                    game.State = board_txt
                    game.Length = length
                    Moves = game.Moves+"\n"+Move
                    game.Moves = Moves
                    game.last_move=Move
                    game.Ongoing= not ended
                    if ended:
                        game.Winner= winner
                    game.save()

                    output_data  = json.dumps({
                        'Code':Code,
                        'State': game.State,
                        'last_move': Move,
                        'Current_Player':Current_Player})
                    return moved,output_data
                else:
                    output_data  = json.dumps({
                        'Code':Code,
                        'State': game.State,
                        'last_move': "",
                        'Current_Player':Current_Player})
                    return moved,output_data
                    # return Response(GameMoveSerializer(game).data,status = status.HTTP_202_ACCEPTED)
        # return moved, json.dumps({'Bad Request': 'Invalid data...'})
        # return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)