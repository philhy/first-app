# Generated by Django 4.2.16 on 2024-12-18 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nflteamstats',
            name='game_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
