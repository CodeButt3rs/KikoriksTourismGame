from atexit import register
from django import template

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