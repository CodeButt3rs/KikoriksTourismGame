from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import GameCycle, Kikorik, Attractions
# Other fuctions


# Create your views here.
def baseTemplate(request):
    return render(request, 'GameApp/base.html')

def indexPage(request):
    return render(request, 'GameApp/index.html')

def gamePage(request):
    if request.user.is_anonymous:
        return redirect('GameAppLogin')
    else:
        context = {'isKikorikAttached': True}
        try:
            kikorikToRender = Kikorik.objects.get(user = request.user)
        except:
            context['isKikorikAttached'] = False
            return render(request, 'GameApp/game.html', context = context)
        kikorikToRender = Kikorik.objects.get(user = request.user)
        currentGameCycle = GameCycle.objects.filter(usersInGame = request.user)
        context['kikorik'] = kikorikToRender
        context['currentGameCycle'] = currentGameCycle[0]
        return render(request, 'GameApp/game.html', context = context)

def loginView(request):
    if request.user.is_authenticated:
        return redirect('GameAppGame')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('GameAppGame')
        else:
            form = AuthenticationForm()
        return render(request, 'GameApp/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('GameAppIndex')
