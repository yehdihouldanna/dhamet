# Generated by Django 3.2.12 on 2022-03-03 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DhametCode', '0010_auto_20220222_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='creator_time',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='game',
            name='opponent_time',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
    ]
