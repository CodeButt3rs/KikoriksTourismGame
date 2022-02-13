# Generated by Django 4.0.2 on 2022-02-13 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attractions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тур. объект')),
                ('recreationK', models.FloatField(verbose_name='Рекреация')),
                ('healthK', models.FloatField(verbose_name='Лечебн.-оздоров.')),
                ('cultureK', models.FloatField(verbose_name='Культ.-познават.')),
                ('sportK', models.FloatField(verbose_name='Спортивный')),
                ('eventsK', models.FloatField(verbose_name='Событийный')),
                ('fatigue', models.FloatField(verbose_name='Усталость')),
                ('gameDay', models.IntegerField(verbose_name='Игровой день')),
            ],
            options={
                'verbose_name': 'Тур. объект',
                'verbose_name_plural': 'Тур. объекты',
            },
        ),
        migrations.CreateModel(
            name='Kikorik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя Смешарика')),
                ('recreationK', models.FloatField(verbose_name='Рекреация')),
                ('healthK', models.FloatField(verbose_name='Лечебн.-оздоров.')),
                ('cultureK', models.FloatField(verbose_name='Культ.-познават.')),
                ('sportK', models.FloatField(verbose_name='Спортивный')),
                ('eventsK', models.FloatField(verbose_name='Событийный')),
                ('fatigue', models.FloatField(verbose_name='Усталость')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Смешарик',
                'verbose_name_plural': 'Смешарики',
            },
        ),
        migrations.CreateModel(
            name='GameCycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameDays', models.IntegerField(verbose_name='Кол-во игровых дней')),
                ('currentGameDay', models.IntegerField(verbose_name='Текущий игровой день')),
                ('attractions', models.ManyToManyField(related_name='attractionss', to='GameApp.Kikorik', verbose_name='Смешарики')),
                ('kikoriks', models.ManyToManyField(related_name='kikoriks', to='GameApp.Kikorik', verbose_name='Смешарики')),
            ],
        ),
    ]
