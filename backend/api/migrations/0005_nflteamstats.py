# Generated by Django 4.2.16 on 2024-12-11 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_prediction_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='NFLTeamStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=255)),
                ('season', models.IntegerField()),
                ('week', models.IntegerField(blank=True, null=True)),
                ('total_snaps', models.IntegerField()),
                ('yards_gained', models.FloatField()),
                ('touchdown', models.IntegerField()),
                ('extra_point_attempt', models.IntegerField()),
                ('field_goal_attempt', models.IntegerField()),
                ('total_points', models.FloatField()),
                ('td_points', models.FloatField()),
                ('xp_points', models.FloatField()),
                ('fg_points', models.FloatField()),
                ('fumble', models.IntegerField()),
                ('fumble_lost', models.IntegerField()),
                ('shotgun', models.IntegerField()),
                ('no_huddle', models.IntegerField()),
                ('qb_dropback', models.IntegerField()),
                ('pass_snaps_count', models.IntegerField()),
                ('pass_snaps_pct', models.FloatField()),
                ('pass_attempts', models.IntegerField()),
                ('complete_pass', models.IntegerField()),
                ('incomplete_pass', models.IntegerField()),
                ('air_yards', models.FloatField()),
                ('passing_yards', models.FloatField()),
                ('pass_td', models.IntegerField()),
                ('interception', models.IntegerField()),
                ('targets', models.IntegerField()),
                ('receptions', models.IntegerField()),
                ('receiving_yards', models.FloatField()),
                ('yards_after_catch', models.FloatField()),
                ('receiving_td', models.IntegerField()),
                ('pass_fumble', models.IntegerField()),
                ('pass_fumble_lost', models.IntegerField()),
                ('rush_snaps_count', models.IntegerField()),
                ('rush_snaps_pct', models.FloatField()),
                ('qb_scramble', models.IntegerField()),
                ('rushing_yards', models.FloatField()),
                ('run_td', models.IntegerField()),
                ('run_fumble', models.IntegerField()),
                ('run_fumble_lost', models.IntegerField()),
                ('home_wins', models.IntegerField(blank=True, null=True)),
                ('home_losses', models.IntegerField(blank=True, null=True)),
                ('home_ties', models.IntegerField(blank=True, null=True)),
                ('away_wins', models.IntegerField(blank=True, null=True)),
                ('away_losses', models.IntegerField(blank=True, null=True)),
                ('away_ties', models.IntegerField(blank=True, null=True)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('win_pct', models.FloatField()),
                ('record', models.CharField(blank=True, max_length=50, null=True)),
                ('yps', models.FloatField()),
            ],
        ),
    ]
