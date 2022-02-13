# import

# from ... import ..
from django.contrib import admin
from .models import Kikorik, Attractions, GameCycle
# Register your models here.

class KikorikAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'happinesK', 'recreationK', 'healthK', 'cultureK', 'sportK', 'eventsK', 'fatigue']

class AttractionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'gameDay', 'recreationK', 'healthK', 'cultureK', 'sportK', 'eventsK', 'fatigue']
admin.site.register(Kikorik, KikorikAdmin)
admin.site.register(Attractions, AttractionsAdmin)
admin.site.register(GameCycle)