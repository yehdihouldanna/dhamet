""" this file contains the consumers for the web sockets which allows
for multiple players to connect to the same game.
"""
import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils.Board import State
from .utils.Players import Dummy , MinMax, Random_plus
from DhametCode.models import Game
from users.models import User
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger('root')
# This is a functional chat consumer could be use later to add a chat functionality.
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
        message = str(self.user) +" says : "+ text_data_json['message']+"\n"
        # logger.info(message)
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


AI_NAMES = ["AI_Random","AI_Dummy","AI_MinMax"]
BOT_NAMES= ["Med10","Mariem","Sidi","احمد","Khadijetou","Cheikh","Vatimetou","ابراهيم",
            "Mamadou","Oumar","Amadou","3abdellahi","Va6me","Moussa","Aly","Samba"]

class GameConsumer(AsyncWebsocketConsumer):
    # TODO : Migrate the code to the model file (to follow the norm : FAT models skinny views)
    def __init__(self):
        super().__init__()
    async def connect(self):
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.user = self.scope['user']
        self.game_group_name = f"game_{self.game_code}"
        logger.info(f"['f' : connect]['user': {self.user}]['channel': {self.game_group_name}]")
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
        message = f"['f': receive]['user': {str(self.user)}]['data': {text_data_json}]"
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
        # Send message to WebSocket
        await self.send(text_data = event['data'])

    @database_sync_to_async
    def post_move(self , text_data_json):
        user = self.scope['user']
        # data = event["data"]
        data = text_data_json
        # logger.info(f"['f': post_move]['user ': {user.username}]['data':{data}]")
        id = data["id"]
        if user.is_authenticated:
            user = User.objects.filter(username = user.username)[0]
        else:
            user = User.objects.filter(username = "Guest")[0]
        if id!="":
            queryset = Game.objects.filter(id=id)
            if queryset.exists():
                game = queryset[0]

                #? Game already completed :
                if game.completed:
                    return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

                #? -------------------------
                #? Timer request :
                #? -------------------------
                try :
                    assert data['type']=="timer"
                    current_turn_  = data['current_turn']
                    game.update_timers(current_turn_)
                    return game.timer_request_response()
                except:
                    pass

                #? -------------------------
                #? Normal (Move) request:
                #? -------------------------
                tier = 0
                try :
                    tier = int(data["tier"])
                except:
                    pass

                try:
                    move = data['last_move']
                    souffle_move = data['souffle_move']
                    # logger.info(f"['f': post_move]['move': {move}]")
                    current_turn = game.current_turn
                    length = game.length
                    board = game.state
                    game_instance = State(n=9,board=board,player = current_turn, length=length,souffle=True)

                    #? User is playing :
                    if ((game.creator==user and current_turn==0) or (game.opponent == user and current_turn)): # * user is playing
                        return game.update_game(id,user,game_instance,move,souffle_move)

                    #? The AI is playing :
                    elif ((game.opponent.username in AI_NAMES and current_turn) or (game.creator.username in AI_NAMES and current_turn==0)): # * the AI is playing
                        Agent = MinMax("AI",current_turn,depth=2)
                        if game.opponent.username == AI_NAMES[0] or game.opponent.username ==AI_NAMES[0]:
                            Agent = Random_plus('AI',current_turn)
                        elif game.opponent.username == AI_NAMES[1] or game.opponent.username ==AI_NAMES[1]:
                            Agent = Dummy('AI',current_turn)

                        move = Agent.move(game_instance)
                        logger.info(f"['f': post_move]['AI_move': {move}]")
                        user_ = game.creator if game.creator.username in AI_NAMES else game.opponent
                        return game.update_game(id,user_,game_instance,move,souffle_move)

                    #? The bot is playing :
                    elif (tier and current_turn==1 ):
                        if tier ==1:
                            Agent = Random_plus("",current_turn)
                        elif tier==2:
                            Agent = Dummy("",current_turn)
                        elif tier ==3: # can be used for ML agent
                            Agent = MinMax("",current_turn,depth=2)
                        else: # just in order to prevent erros
                            Agent = MinMax("________",current_turn,depth=2)
                        move = Agent.move(game_instance)
                        logger.debug(f"['f': post_move]['AI_move': {move}]")
                        user_ = game.creator if game.creator.username in BOT_NAMES else game.opponent
                        return game.update_game(id,user_,game_instance,move,souffle_move)

                    #? Refrech request
                    elif ((game.creator==user and current_turn==1) or (game.opponent == user and current_turn==0)): #* case a user tries a move when it't turn only happens at start when user joins a new game
                        return game.update_game(id,user,game_instance,move="",souffle_move="")
                except:
                    pass
            # raise Exception(f"user {user.username} tried to make a non valid move!")
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        # raise Exception("You can't make a move in a non existing game!!")
