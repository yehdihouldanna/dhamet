from django.urls import path, re_path
from .views import  jouer_f, Intro_Fr, game, main, regles_Ar, regles_Fr,sign_in, docs_Ar,docs_Fr, Intro_Ar, sign_up

urlpatterns = [           
    path('',main),


    #TODO correct the urls in the html file 
    path('jouer.html',game),

    path('authentication/layouts/basic/sign-in.html/',sign_in),
    path('authentication/layouts/basic/sign-up.html',sign_up),

    path('documentation/getting-started_Fr.html',docs_Fr),
    path('documentation/getting-started_Ar.html',docs_Ar),

    path('documentation/getting-started/build/gulp.html',Intro_Ar),
    path('documentation/getting-started/build/gulp_Fr.html',Intro_Fr),

    path('documentation/base/utilities.html',regles_Ar),
    path('documentation/base/utilities_Fr.html',regles_Fr),

    path('jeu.html',jouer_f),


    
    
    path('sign-in',sign_in),
    # re_path(r'(?P<game_code>\w+)/$',main),
    # path('*.html/',main),
    re_path(r'[a-z,A-Z,\/,-,_]+.html/',main),
    path('game',main),
    path('game/',main),
    # re_path(r'game/?([A-Z])\w+',main),
    re_path(r'game/(?P<game_code>\w+)/$',main),
] 