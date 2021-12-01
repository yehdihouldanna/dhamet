from django.shortcuts import render
from termcolor import cprint
# Create your views here.

def main(request,*args,**kwargs):
    # return render(request, 'index.html', {})

    outputs = {}
    print(f"The request path is  {request.path[6:-1]}")
    if ".html" in request.path :
        cprint("condition  verified [_/]" , color ="green")
        return render(request,request.path[6:-1],outputs)

    if len(kwargs):
        outputs = {'game_code': kwargs['game_code']}
    return render(request,"index.html",outputs)
    

def game(request):
    return render(request,"jouer.html")


def dumb_treat_html_links(request,*args,**kwargs):
    return render(request,)
def sign_in(request):
    return render(request,"authentication/layouts/basic/sign-in.html")

def sign_up(request):
    return render(request,"authentication/layouts/basic/sign-up.html")


def docs_Fr(request):
    return render(request,"documentation/getting-started_Fr.html")
    
def docs_Ar(request):
    return render(request,"documentation/getting-started_Ar.html")


def regles_Ar(request):
    return render(request,"documentation/base/utilities.html")
   
def regles_Fr(request):
    return render(request,"documentation/base/utilities_Fr.html")

   
def Intro_Ar(request):
    return render(request,"documentation/getting-started/build/gulp.html")
def Intro_Fr(request):
    return render(request,"documentation/getting-started/build/gulp_Fr.html")




    