from django.db import models

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
    game_date = models.DateField(null=True, blank=True)

class NFLPlayerStats(models.Model):
    team = models.CharField(max_length=50)
    player_id = models.CharField(max_length=50)
    player_name = models.CharField(max_length=100)
    position = models.CharField(max_length=20)
    season = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    game_type = models.CharField(max_length=20)
    pass_attempts = models.PositiveIntegerField(default=0)
    complete_pass = models.PositiveIntegerField(default=0)
    incomplete_pass = models.PositiveIntegerField(default=0)
    passing_yards = models.PositiveIntegerField(default=0)
    passing_air_yards = models.PositiveIntegerField(default=0)
    pass_td = models.PositiveIntegerField(default=0)
    interception = models.PositiveIntegerField(default=0)
    pass_fumble_lost = models.PositiveIntegerField(default=0)
    targets = models.PositiveIntegerField(default=0)
    receptions = models.PositiveIntegerField(default=0)
    receiving_yards = models.PositiveIntegerField(default=0)
    receiving_air_yards = models.PositiveIntegerField(default=0)
    yards_after_catch = models.PositiveIntegerField(default=0)
    reception_td = models.PositiveIntegerField(default=0)
    reception_fumble_lost = models.PositiveIntegerField(default=0)
    rush_attempts = models.PositiveIntegerField(default=0)
    rushing_yards = models.PositiveIntegerField(default=0)
    run_td = models.PositiveIntegerField(default=0)
    run_fumble_lost = models.PositiveIntegerField(default=0)
    fantasy_points_ppr = models.FloatField(default=0.0)
    air_yards_share = models.FloatField(default=0.0)
    target_share = models.FloatField(default=0.0)
    comp_pct = models.FloatField(default=0.0)
    int_pct = models.FloatField(default=0.0)
    pass_td_pct = models.FloatField(default=0.0)
    ypa = models.FloatField(default=0.0)
    rec_td_pct = models.FloatField(default=0.0)
    yptarget = models.FloatField(default=0.0)
    ypr = models.FloatField(default=0.0)
    rush_td_pct = models.FloatField(default=0.0)
    ypc = models.FloatField(default=0.0)
    touches = models.PositiveIntegerField(default=0)
    total_tds = models.PositiveIntegerField(default=0)
    td_pct = models.FloatField(default=0.0)
    total_yards = models.PositiveIntegerField(default=0)
    yptouch = models.FloatField(default=0.0)
    passer_rating = models.FloatField(default=0.0)
    opponent = models.CharField(max_length=50)
    offense_pct = models.FloatField(default=0.0)
    draft_year = models.PositiveIntegerField(null=True, blank=True)
    draft_round = models.PositiveIntegerField(null=True, blank=True)
    draft_pick = models.PositiveIntegerField(null=True, blank=True)
    draft_ovr = models.PositiveIntegerField(null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    adot = models.FloatField(default=0.0)