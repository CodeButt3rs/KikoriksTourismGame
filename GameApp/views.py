from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import GameCycle, Kikorik, Attractions, MakeTurn
from .forms import MakeTurnForm
# Other fuctions

def checkGameFormForDuplicates(form):
    if form.is_valid():
        attractionsList = [
            form['attractionOne'].value(),
            form['attractionTwo'].value(),
            form['attractionThree'].value(),
            form['attractionFour'].value(),
            form['attractionFive'].value()
        ]
        for i in attractionsList:
            loopList = attractionsList
            loopList.remove(i)
            if i in loopList:
                return False
    return True

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
        attractionsInCurrentTurn = Attractions.objects.filter(gameDay = currentGameCycle[0].currentGameDay)
        if request.method == 'POST':
            makeTurnInst = MakeTurn(user=request.user, gameDay = currentGameCycle[0].currentGameDay)
            form = MakeTurnForm(data=request.POST, instance=makeTurnInst)
            if form.is_valid():
                if checkGameFormForDuplicates(form) != True: 
                    return redirect("GameAppGame")
                kikorikToRender.isTurnMade = False
                kikorikToRender.save()
                form.save()
                return redirect('GameAppGame')
        else:
            form = MakeTurnForm()
        context['kikorik'] = kikorikToRender
        context['currentGameCycle'] = currentGameCycle[0]
        context['attractions'] = attractionsInCurrentTurn
        context['attractionsForm'] = form
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

def adminPage(request):
    return render(request, 'GameApp/base.html')
