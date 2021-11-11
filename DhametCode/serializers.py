from django.utils.translation import override
from rest_framework import  serializers
from .models import Game
from rest_framework.exceptions import ValidationError

class GameSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = Game
        # fields =('id','Code','DateTime','Players','Length','Moves')
        fields =('id','Code','DateTime','player1','player2','Length','Moves')

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
       # we will send a request /create-game 
        model = Game
        fields = ('Code','player1','player2')

        @override
        def is_valid(self, raise_exception=False):
            ret = super(CreateGameSerializer, self).is_valid(False)
            if self._errors:
                print("Serialization failed due to {}".format(self.errors))
                if raise_exception:
                    raise ValidationError(self.errors)
            return ret

class GameMoveSerializer(serializers.ModelSerializer):
    Player = serializers.IntegerField(write_only=True)
    class Meta:
        model = Game
        fields = ('Code','State','Player','last_move')
