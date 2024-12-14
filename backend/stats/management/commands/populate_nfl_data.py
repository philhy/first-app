from django.core.management.base import BaseCommand
from ...models import NFLTeamStats
import nfl_data_py as nfl
import pandas as pd

class Command(BaseCommand):
    help = 'Populate NFLTeamStats database with weekly data'

    def handle(self, *args, **options):
        weekly_data = nfl.import_weekly_data([2024]).fillna(0)

        data_to_insert = []
        for _, row in weekly_data.iterrows():
            data_to_insert.append(NFLTeamStats(
                team=row['team'],
                season=row['season'],
                week=row['week'],
                total_snaps=row['total_snaps'],
                yards_gained=row['yards_gained'],
                touchdown=row['touchdown'],
                extra_point_attempt=row['extra_point_attempt'],
                field_goal_attempt=row['field_goal_attempt'],
                total_points=row['total_points'],
                td_points=row['td_points'],
                xp_points=row['xp_points'],
                fg_points=row['fg_points'],
                fumble=row['fumble'],
                fumble_lost=row['fumble_lost'],
                shotgun=row['shotgun'],
                no_huddle=row['no_huddle'],
                qb_dropback=row['qb_dropback'],
                pass_snaps_count=row['pass_snaps'],
                pass_snaps_pct=row['pass_snaps_pct'],
                pass_attempts=row['pass_attempts'],
                complete_pass=row['complete_pass'],
                incomplete_pass=row['incomplete_pass'],
                air_yards=row['air_yards'],
                passing_yards=row['passing_yards'],
                pass_td=row['pass_td'],
                interception=row['interception'],
                targets=row['targets'],
                receptions=row['receptions'],
                receiving_yards=row['receiving_yards'],
                yards_after_catch=row['yards_after_catch'],
                receiving_td=row['receiving_td'],
                pass_fumble=row['pass_fumble'],
                pass_fumble_lost=row['pass_fumble_lost'],
                rush_snaps_count=row['rush_snaps'],
                rush_snaps_pct=row['rush_snaps_pct'],
                qb_scramble=row['qb_scramble'],
                rushing_yards=row['rushing_yards'],
                run_td=row['run_td'],
                run_fumble=row['run_fumble'],
                run_fumble_lost=row['run_fumble_lost'],
                wins=row['wins'],
                losses=row['losses'],
                ties=row['ties'],
                win_pct=row['win_pct'],
                yps=row['yps']
            ))

        NFLTeamStats.objects.bulk_create(data_to_insert)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated NFLTeamStats with {len(data_to_insert)} records!'))