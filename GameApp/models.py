# import

# from ... import ...
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Kikorik(models.Model):

    name = models.CharField("Имя Смешарика", max_length=50)
    icon = models.ImageField("Фотография", null=True)
    description = models.TextField("Описание смешарика", null=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", blank=True, null=True, on_delete=models.CASCADE)
    happinesK = models.FloatField("HK", default=0.5)
    recreationK = models.FloatField("Рекреация (R)")
    healthK = models.FloatField("Лечебн.-оздоров. (H)")
    cultureK = models.FloatField("Культ.-познават. (C)")
    sportK = models.FloatField("Спортивный (S)")
    eventsK = models.FloatField("Событийный (E)")
    fatigue = models.FloatField("Усталость (F)")
    isTurnMade = models.BooleanField("Персонаж сходил?", default=False)

    class Meta:
        verbose_name = ("Смешарик")
        verbose_name_plural = ("Смешарики")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kikorik_detail", kwargs={"pk": self.pk})

class Attractions(models.Model):

    name = models.CharField("Тур. объект (A)", max_length=50)
    icon = models.ImageField("Фотография", null=True)
    recreationK = models.FloatField("Рекреация (R)")
    healthK = models.FloatField("Лечебн.-оздоров. (H)")
    cultureK = models.FloatField("Культ.-познават. (C)")
    sportK = models.FloatField("Спортивный (S)")
    eventsK = models.FloatField("Событийный (E)")
    fatigue = models.FloatField("Усталость (F)")
    gameDay = models.IntegerField("Игровой день (GDay)", default=1)

    class Meta:
        verbose_name = ("Тур. объект")
        verbose_name_plural = ("Тур. объекты")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("attraction_detail", kwargs={"pk": self.pk})

class GameCycle(models.Model):

    name = models.CharField("Название", max_length=50, null=True)
    isActive = models.BooleanField("Игра активна?", default=False)
    isPaused = models.BooleanField("Игра на паузе?", default=False)
    isEnded = models.BooleanField("Игра закончилась?", default=False)
    gameDate = models.DateField("Дата проведения", blank=True, null=True)
    gameDays = models.IntegerField("Кол-во игровых дней")
    currentGameDay = models.IntegerField("Текущий игровой день")
    usersInGame = models.ManyToManyField(User, verbose_name="Пользователи", related_name='usersInGame')

    def __str__(self):
        return str(self.pk)