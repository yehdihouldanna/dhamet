from django.urls import path
from . import views

 # app name 'DhametCode/' will be routed to the included path.
# URLConf
urlpatterns = [
    path('username',views.get_username),
    path('hello/',views.say_hello),
    path('game' , views.GameView.as_view()),
    # path('<str:game_name>' , views.GameView.as_view() , name="game",),
    path('create-game' , views.CreateGameView.as_view()),

#-----------------------------------------------
    # path('move',views.GameMoveView.as_view()),
    path('move/<str:game_code>',views.GameMoveView.as_view(),name="move"),
    # path('game/<str:game_code>',views.GameMoveView.as_view(),name="game"),
#-----------------------------------------------
    path('', views.index, name='index'),
    path('chat/<str:room_name>', views.room, name='room',),
]

