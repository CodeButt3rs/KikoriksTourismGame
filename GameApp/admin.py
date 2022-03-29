# import

# from ... import ..
from django.contrib import admin
from .models import Kikorik, Attractions, GameCycle, MakeTurn, MadeTurn
# Register your models here.

class KikorikAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'happinesK', 'recreationK', 'healthK', 'cultureK', 'sportK', 'eventsK', 'ecoK', 'fatigue']

class AttractionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'gameDay', 'isForRelax', 'recreationK', 'healthK', 'cultureK', 'sportK', 'eventsK', 'ecoK','fatigue']

class GameCycleAdmin(admin.ModelAdmin):
    list_display = ['name', 'gameDays', 'currentGameDay', 'get_amount_of_kikoriks', 'gameDate']

    def get_amount_of_kikoriks(self, obj):
        return obj.usersInGame.count()

    get_amount_of_kikoriks.short_description = 'Пользователей в игре'

admin.site.register(Kikorik, KikorikAdmin)
admin.site.register(Attractions, AttractionsAdmin)
admin.site.register(GameCycle, GameCycleAdmin)
admin.site.register(MakeTurn)
admin.site.register(MadeTurn)