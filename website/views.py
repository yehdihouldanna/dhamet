from django.shortcuts import render
# Create your views here.

def main(request,*args,**kwargs):
    # return render(request, 'index.html', {})

    outputs = {}
    print(f"The request path is  {request.path[5:]}")
    if ".html" in request.path :
        return render(request,request.path,outputs)

    if len(kwargs):
        outputs = {'game_code': kwargs['game_code']}
    return render(request,"index.html",outputs)
    

def sign_in(request):
    return render(request,"authentication/layouts/basic/sign-in.html")

def sign_up(request):
    return render(request,"authentication/layouts/basic/sign-out.html")


def docs_Fr(request):
    return render(request,"Documentation/getting-started_Fr.html")
    
def docs_Ar(request):
    return render(request,"Documentation/getting-started_Ar.html")


def regles_Ar(request):
    return render(request,"Documentation/base/utilities.html")
   
def regles_Fr(request):
    return render(request,"Documentation/base/utilities_Fr.html")

   
def Intro_Ar(request):
    return render(request,"Documentation/getting-started/build/gulp.html")
def Intro_Fr(request):
    return render(request,"Documentation/getting-started/build/gulp_Fr.html")




    