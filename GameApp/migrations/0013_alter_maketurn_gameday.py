# Generated by Django 4.0.2 on 2022-02-15 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameApp', '0012_maketurn_madeturn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maketurn',
            name='gameDay',
            field=models.IntegerField(blank=True, null=True, verbose_name='Игровой день'),
        ),
    ]
