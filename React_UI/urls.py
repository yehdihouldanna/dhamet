
from django.urls import path, re_path
from .views import  index, start_game

urlpatterns = [           
    path('',index),
    path('game',index),
    path('game/',index),
    # re_path(r'game/?([A-Z])\w+',index),
    re_path(r'game/(?P<game_code>\w+)/$',index),
    # path('game/<str:game_code>/',index, name='game',),
    path('start_game',start_game)
] 