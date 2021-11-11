
from django.urls import path 
from .views import index

urlpatterns = [            # app name 'DhametCode' will be routed to the included path.
    path('',index),
    path('game',index),
] 