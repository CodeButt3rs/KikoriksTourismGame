# Generated by Django 4.0.2 on 2022-02-16 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GameApp', '0012_maketurn_madeturn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='madeturn',
            old_name='attractionFive5',
            new_name='attractionFive',
        ),
        migrations.RenameField(
            model_name='madeturn',
            old_name='attractionFour4',
            new_name='attractionFour',
        ),
        migrations.RenameField(
            model_name='madeturn',
            old_name='attractionOne1',
            new_name='attractionOne',
        ),
        migrations.RenameField(
            model_name='madeturn',
            old_name='attractionThree3',
            new_name='attractionThree',
        ),
        migrations.RenameField(
            model_name='madeturn',
            old_name='attractionTwo2',
            new_name='attractionTwo',
        ),
    ]
