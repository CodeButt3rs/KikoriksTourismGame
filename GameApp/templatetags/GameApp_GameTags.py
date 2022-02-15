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
