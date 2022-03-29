# import ...
# from ... import ...
from django.urls import path, include
from .views import *

urlpatterns = [
    path('base', baseTemplate, name='GameAppBase'),
    path('', indexPage, name = "GameAppIndex"),
    path('game', gamePage, name = "GameAppGame"),
    path('login', loginView, name = "GameAppLogin"),
    path('logout', logoutView, name = "GameAppLogout"),
    path('adminpanel', adminPage, name="GameAppAdmin"),
    path('adminpanel/pausegame', pauseGame, name='GameAppPause'),
    path('adminpanel/nextgameday', nextGameDay, name='GameAppNextDay'),
    path('adminpanel/endgame', endGame, name='GameAppEndGame'),
    path('adminpanel/startgame', startGame, name='GameAppStartGame'),
    path('adminpanel/calculate', turnMakingMethod, name='GameAppCalculateGame')
]
