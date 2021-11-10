# Generated by Django 2.2.5 on 2021-11-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Image', models.ImageField(upload_to='images')),
                ('Email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(default='', max_length=10, unique=True)),
                ('DateTime', models.DateTimeField(auto_now_add=True)),
                ('Current', models.IntegerField(default=0)),
                ('Length', models.IntegerField(default=0)),
                ('Moves', models.TextField(default='', max_length=10000)),
                ('Ongoing', models.BooleanField(default=False)),
                ('Winner', models.IntegerField(blank=True, null=True)),
                ('Players', models.ManyToManyField(to='DhametCode.Player')),
            ],
        ),
    ]
