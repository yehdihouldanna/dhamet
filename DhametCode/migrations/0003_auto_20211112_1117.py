# Generated by Django 2.2.5 on 2021-11-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DhametCode', '0002_game_current_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='Current_Player',
            field=models.IntegerField(default=0),
        ),
    ]
