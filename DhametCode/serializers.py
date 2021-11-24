from django.utils.translation import override
from rest_framework import  serializers
from .models import Game
from rest_framework.exceptions import ValidationError

class GameSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Game
        # fields =('id','Code','DateTime','Players','Length','Moves')
        fields =('id','created','completed','creator','opponent','winner','state','length','moves')

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
       # we will send a request /create-game 
        model = Game
        fields = ('id','creator','opponent')

class GameMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','state','last_move','current_turn','winner')
