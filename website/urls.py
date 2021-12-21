from django.urls import path, re_path
from .views import   Intro_Fr, game, main, profile, regles_Ar, regles_Fr,sign_in, docs_Ar,docs_Fr, Intro_Ar, mod_profile , chat_pr , chat_gr

urlpatterns = [
    path('',main),


    #TODO correct the urls in the html file
    path('jouer.html',game),

    # path('authentication/layouts/basic/sign-in.html/',sign_in),
    # path('authentication/layouts/basic/sign-up.html',sign_up),
    path('getting-started_Ar/',docs_Ar, name="docs-ar"),
    path('getting-started_Fr/',docs_Fr, name="docs-fr"),

    path('getting-started/build/gulp/',Intro_Ar, name="intro-fr"),
    path('getting-started/build/gulp_Fr/',Intro_Fr, name="intro-fr"),

    path('base/utilities/',regles_Ar, name="regle-ar"),
    path('base/utilities_Fr/',regles_Fr, name="regle-fr"),

    path('account/overview/',profile, name="profile"),
    path('account/settings/',mod_profile, name="mod_profile"),

    path('apps/chat/private/',chat_pr, name="chat_pr"),
    path('apps/chat/group/',chat_gr, name="chat_gr"),

    # path('jeu.html',jouer_f),
    path('sign-in',sign_in),
    # path('getting-started_Ar',docs_Ar),
    # re_path(r'(?P<game_code>\w+)/$',main),
    # path('*.html/',main),
    re_path(r'[a-z,A-Z,\/,-,_]+.html/',main),
    path('game',main),
    path('game/',main),
    # re_path(r'game/?([A-Z])\w+',main),
    re_path(r'game/(?P<game_code>\w+)/$',main),
]
