from django.db.models import fields
from rest_framework import  serializers
from .models import Game , Player

class GameSerializer(serializers.ModelSerializer):
    class Meta :
        model = Game
        fields =('id','Code','DateTime','Players','Length','Moves')
