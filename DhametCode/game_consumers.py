""" this file contains the consumers for the web sockets which allows
for multiple players to connect to the same game.
"""
import logging
# import coloredlogs
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
from datetime import datetime


logging.basicConfig(filename="./logs/debug.log")
logger = logging.getLogger(__file__)
# coloredlogs.install(level='INFO', logger=logger)
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
        logger.info("the received data is : ",text_data_json)
        message = str(self.user) +" says : "+ tdj['message']+"\n"
        logger.info(message)
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
    def __init__(self):
        super().__init__()
        """ Due to some specific problem with the websocket we need to creat some specif variable for this class"""
        self.ws_first = True
        self.last_move_data = {}
    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.user = self.scope['user']
        self.game_group_name = f"game_{self.game_code}"
        logger.info(f"The user {self.user} connected to the channel : {self.game_group_name}")
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
        logger.info("the received data is : ",text_data_json)
        message = f" {str(self.user)} is requesting a move : "
        logger.info(message)
        output_data = await self.post_move(text_data_json)
        # Send message to game group
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'move_message',
                'data': output_data
            }
        )
    # Receive message from game group
    async def move_message(self, event):
        logger.info("entering the move message method")
        # data = event['data']
        # sender = self.scope["user"].username
        # receiver = self.scope['path'].split('_')[1]
        # output_data = await self.post_move(event)
        # Send message to WebSocket
        await self.send(text_data = event['data'])

    def update_game(self,id,user,game,game_instance,move):
        if move =="":
            winner=""
            try:
                winner = game.winner.username
            except:
                pass
            opponent = ""
            try:
                opponent = game.opponent.username
            except:
                pass
            output_data  = json.dumps({
                        'id':id,
                        'state': game.state,
                        'last_move': game.last_move,
                        'current_turn':game.current_turn,
                        'creator' : game.creator.username,
                        'opponent' : opponent,
                        'winner' : winner})

        else:
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
                winner = game.winner.username
            except:
                pass
            output_data  = json.dumps({
                        'id':id,
                        'state': game.state,
                        'last_move': game.last_move,
                        'current_turn':game.current_turn,
                        'creator' : game.creator.username,
                        'opponent' : game.opponent.username,
                        'winner' : winner})
        if self.ws_first:
            logger.debug(f"sending data to the browser : {output_data}")
        else :
            logger.debug(f"sending data to the browser : {output_data}" )
        self.ws_first = not self.ws_first
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
    def post_move(self , text_data_json):
        user = self.scope['user']
        # data = event["data"]
        data = text_data_json
        logger.info(f"Starting the post_move method with sender : {user.username}\n data : {data}")
        id = data["id"]
        if user.is_authenticated:
            user = User.objects.filter(username = user.username)[0]
        else:
            user = User.objects.filter(username = "Guest")[0]
        if id!="":
            queryset = Game.objects.filter(id=id)
            if queryset.exists():
                current_turn_  = data['current_turn']
                move = data['last_move']
                logger.info(f"in the post method move:{move}")
                game = queryset[0]
                current_turn = game.current_turn
                length = game.length
                board = self.deserialize(game.state)
                game_instance = State(n=9,board=board,player = current_turn, length=length)
                AI_NAMES = set(["AI_Random","AI_Dummy","AI_MinMax"])
                if ((game.creator==user and current_turn==0) or (game.opponent == user and current_turn)): # user is playing
                    return self.update_game(id,user,game,game_instance,move)
                elif ((game.opponent.username in AI_NAMES and current_turn) or (game.creator.username in AI_NAMES and current_turn==0)): # the AI is playing
                    # Agent = Random('AI',current_turn)
                    # Agent = Dummy('AI',current_turn)
                    Agent = MinMax("AI",current_turn,depth=2)
                    move = Agent.move(game_instance)
                    logger.info(f"The AI agent moved : {move}")
                    user_ = game.creator if game.creator.username in AI_NAMES else game.opponent
                    return self.update_game(id,user_,game,game_instance,move)
                elif ((game.creator==user and current_turn==1) or (game.opponent == user and current_turn==0)): # case a user tries a move when it't turn only happens at start when user joins a new game
                    return self.update_game(id,user,game,game_instance,move="")
            # raise Exception(f"user {user.username} tried to make a non valid move!")
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        # raise Exception("You can't make a move in a non existing game!!")
