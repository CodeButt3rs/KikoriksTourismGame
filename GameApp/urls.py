# import ...
# from ... import ...
from django.urls import path, include
from .views import baseTemplate, gamePage, indexPage, loginView, logoutView

urlpatterns = [
    path('base', baseTemplate, name='GameAppBase'),
    path('', indexPage, name = "GameAppIndex"),
    path('game', gamePage, name = "GameAppGame"),
    path('login', loginView, name = "GameAppLogin"),
    path('logout', logoutView, name = "GameAppLogout"),
]
