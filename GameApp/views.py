from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import GameCycle, Kikorik, Attractions, MadeTurn, MakeTurn
from .forms import MakeTurnForm
# Other fuctions

def returnTotalHK(attraction, kikorik):
    hk = attraction.recreationK * kikorik.recreationK + attraction.healthK * kikorik.healthK + attraction.sportK * kikorik.sportK + attraction.eventsK * kikorik.eventsK + attraction.ecoK * kikorik.ecoK
    return round(hk, 2)

def calculateHK(fatigue, hk):
    if fatigue < 0:
        hkn = round(hk * (1 + abs(fatigue)), 2)
        return hkn
    hkn = round(hk * fatigue, 2)
    return hkn

def calculateFatigue(fatigue1, fatigue2):
    fatigue = round(fatigue1 - fatigue2, 2)
    if fatigue < -0.3:
        fatigue = -0.3
    elif fatigue > 0.7:
        fatigue = 0.7
        print(fatigue)
    return fatigue

def turnMakingMethod(request):
    cycle = GameCycle.objects.filter(usersInGame = request.user).last()
    kikorikToChange = Kikorik.objects.get(user = request.user)
    # print(cycle.usersInGame.all())
    for i in cycle.usersInGame.all():
        kikorikToChange = Kikorik.objects.get(user = i)
        # print('Итерирую',kikorikToChange)
        makeTurn = MakeTurn.objects.filter(Q(user = i) & Q(gameDay = cycle.currentGameDay)).last()
        if makeTurn is None: #Если хода не было
            kikorikToChange.happinesK = kikorikToChange.happinesK - 0.3
            kikorikToChange.fatigue = kikorikToChange.fatigue - 0.3
            kikorikToChange.save()
            continue
        # print(makeTurn)
        madeTurn = MadeTurn(
            user = makeTurn.user,
            gameDay = makeTurn.gameDay,
            attractionOne = makeTurn.attractionOne,
            attractionTwo = makeTurn.attractionTwo,
            attractionThree = makeTurn.attractionThree,
            attractionFour = makeTurn.attractionFour,
            attractionFive = makeTurn.attractionFive,
        )
        # calculations part
        # print(type(kikorikToChange.fatigue))
        # print(type(madeTurn.fatigueOne))
        # print(type(madeTurn.attractionTwo.fatigue))
        madeTurn.fatigueOne = calculateFatigue(kikorikToChange.fatigue, madeTurn.attractionOne.fatigue)
        madeTurn.fatigueTwo = calculateFatigue(madeTurn.fatigueOne, madeTurn.attractionTwo.fatigue)
        madeTurn.fatigueThree = calculateFatigue(madeTurn.fatigueTwo, madeTurn.attractionThree.fatigue)
        madeTurn.fatigueFour = calculateFatigue(madeTurn.fatigueThree, madeTurn.attractionFour.fatigue)
        madeTurn.fatigueFive = calculateFatigue(madeTurn.fatigueFour, madeTurn.attractionFive.fatigue)
        madeTurn.happinesOne = kikorikToChange.happinesK + calculateHK(kikorikToChange.fatigue, returnTotalHK(madeTurn.attractionOne, kikorikToChange))
        madeTurn.happinesTwo = madeTurn.happinesOne+ calculateHK(madeTurn.fatigueOne, returnTotalHK(madeTurn.attractionTwo, kikorikToChange))
        madeTurn.happinesThree = madeTurn.happinesTwo + calculateHK(madeTurn.fatigueTwo, returnTotalHK(madeTurn.attractionThree, kikorikToChange))
        madeTurn.happinesFour = madeTurn.happinesThree + calculateHK(madeTurn.fatigueThree, returnTotalHK(madeTurn.attractionFour, kikorikToChange))
        madeTurn.happinesFive = madeTurn.happinesFour + calculateHK(madeTurn.fatigueFour, returnTotalHK(madeTurn.attractionFive, kikorikToChange))
        madeTurn.save()
        # print(madeTurn.fatigueOne, madeTurn.attractionOne, returnTotalHK(madeTurn.attractionOne, kikorikToChange), calculateHK(kikorikToChange.fatigue, returnTotalHK(madeTurn.attractionOne, kikorikToChange)))
        # print(madeTurn.fatigueTwo, madeTurn.attractionTwo, returnTotalHK(madeTurn.attractionOne, kikorikToChange), calculateHK(madeTurn.fatigueOne, returnTotalHK(madeTurn.attractionTwo, kikorikToChange)))
        # print(madeTurn.fatigueThree, madeTurn.attractionThree, returnTotalHK(madeTurn.attractionThree, kikorikToChange), calculateHK(madeTurn.fatigueTwo, returnTotalHK(madeTurn.attractionThree, kikorikToChange)))
        # print(madeTurn.fatigueFour, madeTurn.attractionFour, returnTotalHK(madeTurn.attractionFour, kikorikToChange), calculateHK(madeTurn.fatigueThree, returnTotalHK(madeTurn.attractionFour, kikorikToChange)))
        # print(madeTurn.fatigueFive, madeTurn.attractionFive, returnTotalHK(madeTurn.attractionFive, kikorikToChange), calculateHK(madeTurn.fatigueFour, returnTotalHK(madeTurn.attractionFive, kikorikToChange)))
        # print(madeTurn.happinesOne, madeTurn.happinesTwo, madeTurn.happinesThree, madeTurn.happinesFour, madeTurn.happinesFive)
        kikorikToChange.fatigue = madeTurn.fatigueFive
        kikorikToChange.happinesK = madeTurn.happinesFive
        kikorikToChange.save()
    return redirect('GameAppAdmin')

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
                kikorikToRender.isTurnMade = True
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
    if request.user.is_staff == False:
        return redirect('GameAppGame')
    gameCycle = GameCycle.objects.all().last()
    kikoriks = []
    for i in gameCycle.usersInGame.all():
        try:
            kikoriks.append(Kikorik.objects.get(user = i))
        except:
            pass
    
    return render(
        request, 'GameApp/admin.html', 
        context= {
            'cycle': gameCycle,
            'kikoriks': kikoriks
            }
        )

# Управление игрой
def pauseGame(request):
    if request.user.is_staff:
        gameCycle = GameCycle.objects.all().last()
        if gameCycle.isPaused:
            gameCycle.isPaused = False
        else:
            gameCycle.isPaused = True
        gameCycle.save()
        return redirect('GameAppAdmin')
    else:
        return redirect('GameAppAdmin')

def nextGameDay(request):
    if request.user.is_staff:
        gameCycle = GameCycle.objects.all().last()
        if gameCycle.currentGameDay == gameCycle.gameDays:
            return redirect('GameAppAdmin')
        turnMakingMethod(request)
        gameCycle.currentGameDay += 1
        gameCycle.isPaused = False
        gameCycle.save()
        return redirect('GameAppAdmin')
    else:
        return redirect('GameAppAdmin')

def endGame(request):
    if request.user.is_staff:
        gameCycle = GameCycle.objects.all().last()
        if gameCycle.currentGameDay == gameCycle.gameDays and gameCycle.isPaused == True:
            gameCycle.isEnded = True
            gameCycle.isPaused = False
            gameCycle.isActive = False
            gameCycle.save()
            return redirect('GameAppAdmin')
    else:
        return redirect('GameAppAdmin')

def startGame(request):
    if request.user.is_staff:
        gameCycle = GameCycle.objects.all().last()
        if gameCycle.currentGameDay != gameCycle.gameDays:
            gameCycle.isEnded = False
            gameCycle.isPaused = False
            gameCycle.isActive = True
            gameCycle.save()
            return redirect('GameAppAdmin')
    else:
        return redirect('GameAppAdmin')