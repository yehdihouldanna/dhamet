from django.shortcuts import render
# Create your views here.

def index(request,*args , **kwargs):
    # print("this function got called from,",str(request))
    # print(args)
    # print(kwargs)
    if len(kwargs):
        outputs = {'game_code': kwargs['game_code'],}
        return render(request,'frontend/game_online.html',outputs)
    else:
        return render(request,"frontend/index.html")

def start_game(request,*args , **kwargs):
    return render(request,'frontend/start_game.html')
    