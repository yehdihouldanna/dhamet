from django.urls import path, re_path
from .views import  main,sign_in
urlpatterns = [           
    path('',main),


    #TODO correct the urls in the html file 
    path('authentication/layouts/basic/sign-in.html/',sign_in),
    path('sign-in',sign_in),
    # re_path(r'(?P<game_code>\w+)/$',main),
    # path('*.html/',main),
    re_path(r'[a-z,A-Z,\/,-,_]+.html/',main),
    path('game',main),
    path('game/',main),
    # re_path(r'game/?([A-Z])\w+',main),
    re_path(r'game/(?P<game_code>\w+)/$',main),
] 