# Generated by Django 3.2.9 on 2022-02-01 16:45

from django.db import migrations, models
import time


class Migration(migrations.Migration):

    dependencies = [
        ('DhametCode', '0008_game_last_move_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='last_move_time',
            field=models.FloatField(default=time.time),
        ),
    ]
