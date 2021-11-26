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
def docs(request):
    return render(request,"documentation/getting-started.html")


    