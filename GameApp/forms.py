from django import forms
from .models import Attractions, MakeTurn, GameCycle

class MakeTurnForm(forms.ModelForm):

    try:
        currentDay = GameCycle.objects.filter(isActive = True).last().currentGameDay
    except:
        currentDay = 1
    attractionsList = Attractions.objects.filter(gameDay = currentDay)

    attractionOne = forms.ModelChoiceField(
        queryset=attractionsList,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Тур. объект №1',
        empty_label="Пусто")
    attractionTwo = forms.ModelChoiceField(
        queryset=attractionsList,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Тур. объект №2',
        empty_label="Пусто")
    attractionThree = forms.ModelChoiceField(
        queryset=attractionsList,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Тур. объект №3',
        empty_label="Пусто")
    attractionFour = forms.ModelChoiceField(
        queryset=attractionsList,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Тур. объект №4',
        empty_label="Пусто")
    attractionFive = forms.ModelChoiceField(
        queryset=attractionsList,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-sm'
            }
        ),
        label='Тур. объект №5',
        empty_label="Пусто")


    class Meta:
        model = MakeTurn
        fields = ('attractionOne', 'attractionTwo', 'attractionThree', 'attractionFour', 'attractionFive',)
        exclude = ('gameDay','user')
