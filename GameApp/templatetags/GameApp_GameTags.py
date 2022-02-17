from django import template
from django.db.models import Q
from GameApp.models import MadeTurn

register = template.Library()

@register.inclusion_tag('GameApp/_inc/_happinesProgressBar.html',takes_context=True)
def getHappinesProgressBar(context):
    return {'percents': int(context['kikorik'].happinesK * 100)}

@register.inclusion_tag('GameApp/_inc/_fatigueProgressBar.html',takes_context=True)
def getFatigueProgressBar(context):
    return {'percents': int(100 - (0.3 + context['kikorik'].fatigue) * 100)}

@register.inclusion_tag('GameApp/_inc/_gameContext.html',takes_context=True)
def getGameContext(context):
    return context

@register.inclusion_tag('GameApp/_inc/_attractionsCard.html',takes_context=True)
def getAttractionsCard(context):
    return context

@register.inclusion_tag('GameApp/_inc/_attractionCard.html',takes_context=True)
def getDayAttractions(context):
    return context

@register.inclusion_tag('GameApp/_inc/_stars.html', takes_context=False)
def getAmountOfStars(k):
    return {'k': k // 0.2}

@register.inclusion_tag('GameApp/_inc/_antiFatigueBadge.html')
def getAntiFatigueBadge(k):
    return {'percents': int(abs((k.fatigue) * 100))}

@register.inclusion_tag('GameApp/_inc/_FatigueBadge.html')
def getFatigueBadge(k):
    return {'percents': int(abs((k.fatigue) * 100))}

@register.inclusion_tag('GameApp/_inc/_kikoriksInGameChart.html', takes_context=True)
def getKikoriksAdminStats(context, ki):
    kikoriksNames = []
    kikoriksHappines = []
    kikoriksFatigue = []
    for i in ki:
        kikoriksNames.append(i.name)
        kikoriksHappines.append(i.happinesK * 100)
        kikoriksFatigue.append(100 - (0.3 + i.fatigue) * 100)
    return {'names': kikoriksNames, 'happines': kikoriksHappines, 'fatigue': kikoriksFatigue}

@register.inclusion_tag('GameApp/_inc/_kikoriksUsersStats.html', takes_context=True)
def getKikoriksUsersStats(context, ki):
    madeTurns = MadeTurn.objects.filter(user = ki.user)
    attractionsNames = []
    attractionsHappines = []
    attractionsFatigue = []
    if madeTurns.count() is 0:
        return {'isEmpty': True}
    for i in madeTurns:
        attractionsNames.append(f'Д{i.gameDay}: {i.attractionOne.name}')
        attractionsNames.append(f'Д{i.gameDay}: {i.attractionTwo.name}')
        attractionsNames.append(f'Д{i.gameDay}: {i.attractionThree.name}')
        attractionsNames.append(f'Д{i.gameDay}: {i.attractionFour.name}')
        attractionsNames.append(f'Д{i.gameDay}: {i.attractionFive.name}')
        attractionsFatigue.append(100 - (0.3 + i.fatigueOne) * 100)
        attractionsFatigue.append(100 - (0.3 + i.fatigueTwo) * 100)
        attractionsFatigue.append(100 - (0.3 + i.fatigueThree) * 100)
        attractionsFatigue.append(100 - (0.3 + i.fatigueFour) * 100)
        attractionsFatigue.append(100 - (0.3 + i.fatigueFive) * 100)
        attractionsHappines.append(i.happinesOne * 100)
        attractionsHappines.append(i.happinesTwo * 100)
        attractionsHappines.append(i.happinesThree * 100)
        attractionsHappines.append(i.happinesFour * 100)
        attractionsHappines.append(i.happinesFive * 100)
    for j in attractionsHappines:
        if j < 0:
            attractionsHappines[attractionsHappines.index(j)] = 0
    return {
        'isEmpty': False, 
        'names': attractionsNames, 
        'happines': attractionsHappines, 
        'fatigue': attractionsFatigue, 
        'kikorikpk': ki.pk,
        'kikorikname': ki.name,
        'kikorikuser': ki.user}