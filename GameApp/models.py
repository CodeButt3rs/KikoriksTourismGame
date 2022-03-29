# import

# from ... import ...
from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ValidationError

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
    ecoK = models.FloatField("Экологический (Eco)", null=True)
    fatigue = models.FloatField("Усталость (F)")
    isTurnMade = models.BooleanField("Персонаж сходил?", default=False)

    class Meta:
        verbose_name = ("Смешарик")
        verbose_name_plural = ("Смешарики")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kikorik_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        k = abs(self.recreationK) + abs(self.healthK) + abs(self.cultureK) + abs(self.sportK) + abs(self.eventsK) + abs(self.ecoK)
        if k > 2.5:
            return ValidationError("Значение вышло за пределы коэффициента Кати Кадочкиной")
        # Защита от дурака "Счастье"
        if self.happinesK > 1:
            self.happinesK = 1
        elif self.happinesK < 0:
            self.happinesK = 0
        # Защита от дурака "Усталость"
        if self.fatigue > 0.7:
            self.fatigue = 0.7
        elif self.fatigue < -0.3:
            self.fatigue = -0.3
        return super(Kikorik, self).save(*args, **kwargs)

class Attractions(models.Model):

    name = models.CharField("Тур. объект (A)", max_length=50)
    icon = models.ImageField("Фотография", null=True)
    isForRelax = models.BooleanField("Создан для отдыха?", default=False)
    recreationK = models.FloatField("Рекреация (R)")
    healthK = models.FloatField("Лечебн.-оздоров. (H)")
    cultureK = models.FloatField("Культ.-познават. (C)")
    sportK = models.FloatField("Спортивный (S)")
    eventsK = models.FloatField("Событийный (E)")
    ecoK = models.FloatField("Экологический (Eco)", null=True)
    fatigue = models.FloatField("Усталость (F)")
    gameDay = models.IntegerField("Игровой день (GDay)", default=1)

    class Meta:
        verbose_name = ("Тур. объект")
        verbose_name_plural = ("Тур. объекты")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("attraction_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        k = self.recreationK + self.healthK + self.cultureK + self.sportK + self.eventsK + self.ecoK
        if k > 2.5 or k < 0:
            return ValidationError
        self.fatigue = round(0.30 * (k/2.5), 2)
        if self.isForRelax:
            self.fatigue = round(-1.5 * self.fatigue, 2)
        return super(Attractions, self).save(*args, **kwargs)

class GameCycle(models.Model):

    MODS = (
        ('NONE', 'Нету'),
        ('Бафы', (
                ('SUNNY', 'Солнечно (+10% HK)'),
                ('SECRET', 'В планах реализовать')
            )
        ),
        ('Дебафы', (
                ('RAIN', 'Дождь (-10% HK)'),
                ('SUN', 'Жара (+10% F)'),
                ('WIND', 'Ветренно (-15% HK и -15% F)'),
                ('POISON', 'Отравление (+30% F)'),
                ('HURRICANE', 'Ураган (-30% HK)'),
                ('SECRET', 'В планах реализовать')
            )
        )
    )

    name = models.CharField("Название", max_length=50, null=True)
    isActive = models.BooleanField("Игра активна?", default=False)
    isPaused = models.BooleanField("Игра на паузе?", default=False)
    isEnded = models.BooleanField("Игра закончилась?", default=False)
    gameDate = models.DateField("Дата проведения", blank=True, null=True)
    gameDays = models.IntegerField("Кол-во игровых дней")
    currentGameDay = models.IntegerField("Текущий игровой день")
    usersInGame = models.ManyToManyField(User, verbose_name="Пользователи", related_name='usersInGame')
    # gameMod = models.CharField("Модификатор", choices=MODS, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class MakeTurn(models.Model):

    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    gameDay = models.IntegerField("Игровой день", blank=True, null=True)
    attractionOne = models.ForeignKey(Attractions, verbose_name="Достопримечательность №1", related_name="AttractionOne", on_delete=models.CASCADE)
    attractionTwo = models.ForeignKey(Attractions, verbose_name="Достопримечательность №2", related_name="AttractionTwo", on_delete=models.CASCADE)
    attractionThree = models.ForeignKey(Attractions, verbose_name="Достопримечательность №3", related_name="AttractionThree", on_delete=models.CASCADE)
    attractionFour = models.ForeignKey(Attractions, verbose_name="Достопримечательность №4", related_name="AttractionFour", on_delete=models.CASCADE)
    attractionFive = models.ForeignKey(Attractions, verbose_name="Достопримечательность №5", related_name="AttractionFive", on_delete=models.CASCADE)

    def __str__(self):
        string = f"Ход №{self.gameDay} игрока {self.user}"
        return string
    
class MadeTurn(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    gameDay = models.IntegerField("Игровой день", blank=True, null=True)
    attractionOne = models.ForeignKey(Attractions, verbose_name="Достопримечательность №1", related_name="AttractionOne1", on_delete=models.CASCADE, null=True)
    attractionTwo = models.ForeignKey(Attractions, verbose_name="Достопримечательность №2", related_name="AttractionTwo2", on_delete=models.CASCADE, null=True)
    attractionThree = models.ForeignKey(Attractions, verbose_name="Достопримечательность №3", related_name="AttractionThree3", on_delete=models.CASCADE, null=True)
    attractionFour = models.ForeignKey(Attractions, verbose_name="Достопримечательность №4", related_name="AttractionFour4", on_delete=models.CASCADE, null=True)
    attractionFive = models.ForeignKey(Attractions, verbose_name="Достопримечательность №5", related_name="AttractionFive5", on_delete=models.CASCADE, null=True)
    fatigueOne = models.FloatField("Усталость №1")
    fatigueTwo = models.FloatField("Усталость №2")
    fatigueThree = models.FloatField("Усталость №3")
    fatigueFour = models.FloatField("Усталость №4")
    fatigueFive = models.FloatField("Усталость №5")
    happinesOne = models.FloatField("HK №1")
    happinesTwo = models.FloatField("HK №2")
    happinesThree = models.FloatField("HK №3")
    happinesFour = models.FloatField("HK №4")
    happinesFive = models.FloatField("HK №5")

    def __str__(self):
        s = f"Результаты хода №{self.gameDay} игрока {self.user}"
        return s