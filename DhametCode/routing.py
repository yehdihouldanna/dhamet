# chat/routing.py
from django.urls import re_path

from . import game_consumers

# websocket_urlpatterns = [
#     
# ]
websocket_urlpatterns = [
    re_path(r'DhametCode/(?P<room_name>\w+)/$', game_consumers.ChatConsumer.as_asgi()),
    # re_path(r'DhametCode/(?P<room_name>\w+)/$', game_consumers.GameConsumer.as_asgi()),
    # re_path(r"DhametCode/game_+[a-z,A-Z,0-9,_]+/(?P<username>\w+)/$", game_consumers.ChatConsumer.as_asgi()),
    # re_path(r"DhametCode/game_+[a-z,A-Z,0-9,_]+/(?P<username>\w+)/$", game_consumers.ChatConsumer.as_asgi()),
]

####Target pattern for game in re : game_+[a-z,A-Z,0-9,_]+  and /<username>
