from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    CATEGORIES = [
        (0, 'Sports')
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')

    def __str__(self):
        return self.title
    
class NFLTeamStats(models.Model):
    team = models.CharField(max_length=255)
    season = models.IntegerField()
    week = models.IntegerField(null=True, blank=True)
    total_snaps = models.IntegerField()
    yards_gained = models.FloatField()
    touchdown = models.IntegerField()
    extra_point_attempt = models.IntegerField()
    field_goal_attempt = models.IntegerField()
    total_points = models.FloatField()
    td_points = models.FloatField()
    xp_points = models.FloatField()
    fg_points = models.FloatField()
    fumble = models.IntegerField()
    fumble_lost = models.IntegerField()
    shotgun = models.IntegerField()
    no_huddle = models.IntegerField()
    qb_dropback = models.IntegerField()
    pass_snaps_count = models.IntegerField()
    pass_snaps_pct = models.FloatField()
    pass_attempts = models.IntegerField()
    complete_pass = models.IntegerField()
    incomplete_pass = models.IntegerField()
    air_yards = models.FloatField()
    passing_yards = models.FloatField()
    pass_td = models.IntegerField()
    interception = models.IntegerField()
    targets = models.IntegerField()
    receptions = models.IntegerField()
    receiving_yards = models.FloatField()
    yards_after_catch = models.FloatField()
    receiving_td = models.IntegerField()
    pass_fumble = models.IntegerField()
    pass_fumble_lost = models.IntegerField()
    rush_snaps_count = models.IntegerField()
    rush_snaps_pct = models.FloatField()
    qb_scramble = models.IntegerField()
    rushing_yards = models.FloatField()
    run_td = models.IntegerField()
    run_fumble = models.IntegerField()
    run_fumble_lost = models.IntegerField()
    home_wins = models.IntegerField(null=True, blank=True)
    home_losses = models.IntegerField(null=True, blank=True)
    home_ties = models.IntegerField(null=True, blank=True)
    away_wins = models.IntegerField(null=True, blank=True)
    away_losses = models.IntegerField(null=True, blank=True)
    away_ties = models.IntegerField(null=True, blank=True)
    wins = models.IntegerField()
    losses = models.IntegerField()
    ties = models.IntegerField()
    win_pct = models.FloatField()
    record = models.CharField(max_length=50, null=True, blank=True)
    yps = models.FloatField()

    
