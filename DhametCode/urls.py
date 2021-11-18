from django.urls import path
from . import views


# URLConf
urlpatterns = [
    path('hello/',views.say_hello),
    path('game' , views.GameView.as_view()),
    path('create-game' , views.CreateGameView.as_view()),
    path('move',views.GameMoveView.as_view()),
    path('', views.index, name='index'),
    path('<str:room_name>', views.room, name='room',),
]

