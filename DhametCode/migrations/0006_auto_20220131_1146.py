# Generated by Django 3.2.9 on 2022-01-31 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DhametCode', '0005_auto_20220131_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='timer_creator',
            new_name='creator_time',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='timer_opponent',
            new_name='opponent_time',
        ),
    ]
