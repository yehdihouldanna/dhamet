from django.urls import path, re_path
from .views import   Intro_Fr, main, regles_Ar, regles_Fr,sign_in, docs_Ar,docs_Fr, Intro_Ar

urlpatterns = [           
    path('',main),


    #TODO correct the urls in the html file 
    path('authentication/layouts/basic/sign-in.html/',sign_in),
    path('Documentation/getting-started_Fr.html',docs_Fr),
    path('Documentation/getting-started_Ar.html',docs_Ar),

    path('Documentation/getting-started/build/gulp.html',Intro_Ar),
    path('Documentation/getting-started/build/gulp_Fr.html',Intro_Fr),

    path('Documentation/base/utilities.html',regles_Ar),
    path('Documentation/base/utilities_Fr.html',regles_Fr),
    
    path('sign-in',sign_in),
    re_path(r'(?P<game_code>\w+)/$',main),
    path('game',main),
    path('game/',main),
    # re_path(r'game/?([A-Z])\w+',main),
    re_path(r'game/(?P<game_code>\w+)/$',main),
] 