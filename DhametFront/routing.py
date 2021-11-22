# chat/routing.py
from django.urls import re_path

from DhametCode import game_consumers

websocket_urlpatterns = [
    re_path(r'DhametCode/chat/(?P<room_name>\w+)/$', game_consumers.ChatConsumer.as_asgi()),
    re_path(r'DhametCode/move/(?P<game_code>\w+)/$', game_consumers.GameConsumer.as_asgi()),
    re_path(r'DhametCode/game/(?P<game_code>\w+)/$', game_consumers.GameConsumer.as_asgi()),
    re_path(r'DhametCode/game/(?P<game_code>\w+)/move$', game_consumers.GameConsumer.as_asgi()),
]
### game code pattern :  game_+[a-z,A-Z,0-9,_]+ 