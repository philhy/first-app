import os
import django
import nfl_data_py as nfl
import pandas as pd
import concurrent.futures
import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print('Getting environment details')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from stats.models import NFLTeamStats


def importData(data, years):
    date_range = range(years[0], years[1]+1)
    
    print(f'Getting {data} data')
    def getData(i, data=data):
        if 'pbp' in data:
            imported_data = nfl.import_pbp_data([i])
        return imported_data
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, date_range))
    
    print('Creating DataFrame')
    data_df = pd.concat(results)

    return data_df

def sumData(df, i=['run', 'pass']):
    print('Summing data')
    data_dict = {
        'yards_gained': 'sum',
        'shotgun': 'sum',
        'no_huddle': 'sum',
        'qb_dropback': 'sum',
        'fumble_lost': 'sum',
        'fumble': 'sum'
    }

    if isinstance(i, str) and i.upper() == 'RUN':
        for stat in ['qb_scramble', 'rushing_yards', 'touchdown']:
            data_dict[stat] = 'sum'
    elif isinstance(i, str) and i.upper() == 'PASS':
        for stat in ['air_yards', 'incomplete_pass', 'interception', 'complete_pass', 'passing_yards', 'receiving_yards', 'yards_after_catch', 'touchdown']:
            data_dict[stat] = 'sum'
    else:
        for stat in ['qb_scramble', 'rushing_yards', 'air_yards', 'incomplete_pass', 'interception', 'complete_pass', 'passing_yards', 'receiving_yards', 'yards_after_catch']:
            data_dict[stat] = 'sum'

    if isinstance(i, str):
        new_df = df[df.play_type == i].groupby(['posteam', 'season', 'week', 'play_type']).agg(data_dict).unstack(fill_value=0).reset_index()
        new_df.columns = [i[0] for i in new_df.columns]
        new_df = new_df.rename(columns={'posteam': 'team', 'fumble_lost': f'{i}_fumble_lost', 'fumble': f'{i}_fumble', 'touchdown': f'{i}_td'})
    else:
        new_df = df[df.play_type.isin(i)].groupby(['posteam', 'season', 'week']).agg(data_dict).reset_index()

    return new_df

def winLossTotal(row, i):
    wins = row.loc[row[f'{i}_team'] == row['winner'], 'winner'].count()
    losses = row.loc[row[f'{i}_team'] != row['winner'], 'winner'].count()
    ties = len(row[row['winner'] == 'TIE'])
    cols = [f'{i}_wins', f'{i}_losses', f'{i}_ties']
    return pd.Series([wins, losses, ties], index=cols)

def inputTeamData(df):
    print('Adding data to model')
    data = []
    for i in range(len(df)):
        data.append(NFLTeamStats(
            team=df.team.iat[i],
            season=df.season.iat[i],
            week=df.week.iat[i],
            total_snaps=df.total_snaps.iat[i],
            yards_gained=df.yards_gained.iat[i],
            touchdown=df.touchdown.iat[i],
            extra_point_attempt=df.extra_point_attempt.iat[i],
            field_goal_attempt=df.field_goal_attempt.iat[i],
            total_points=df.total_points.iat[i],
            td_points=df.td_points.iat[i],
            xp_points=df.xp_points.iat[i],
            fg_points=df.fg_points.iat[i],
            fumble=df.fumble.iat[i],
            fumble_lost=df.fumble_lost.iat[i],
            shotgun=df.shotgun.iat[i],
            no_huddle=df.no_huddle.iat[i],
            qb_dropback=df.qb_dropback.iat[i],
            pass_snaps_count=df.pass_snaps_count.iat[i],
            pass_snaps_pct=df.pass_snaps_pct.iat[i],
            pass_attempts=df.pass_attempts.iat[i],
            complete_pass=df.complete_pass.iat[i],
            incomplete_pass=df.incomplete_pass.iat[i],
            air_yards=df.air_yards.iat[i],
            passing_yards=df.passing_yards.iat[i],
            pass_td=df.pass_td.iat[i],
            interception=df.interception.iat[i],
            targets=df.targets.iat[i],
            receptions=df.receptions.iat[i],
            receiving_yards=df.receiving_yards.iat[i],
            yards_after_catch=df.yards_after_catch.iat[i],
            receiving_td=df.receiving_td.iat[i],
            pass_fumble=df.pass_fumble.iat[i],
            pass_fumble_lost=df.pass_fumble_lost.iat[i],
            rush_snaps_count=df.rush_snaps_count.iat[i],
            rush_snaps_pct=df.rush_snaps_pct.iat[i],
            qb_scramble=df.qb_scramble.iat[i],
            rushing_yards=df.rushing_yards.iat[i],
            run_td=df.run_td.iat[i],
            run_fumble=df.run_fumble.iat[i],
            run_fumble_lost=df.run_fumble_lost.iat[i],
            wins=df.wins.iat[i],
            losses=df.losses.iat[i],
            ties=df.ties.iat[i],
            win_pct=df.win_pct.iat[i],
            yps=df.yps.iat[i]
        ))

    return data

pbp = importData('pbp', [2012, 2023])

pbp = pbp[pbp.season_type == 'REG']

pbp_filtered = pbp[pbp.play_type.isin(['pass', 'run'])].sort_values(by=['season'])

print('Getting team data')
team_data = pbp_filtered.groupby(['posteam', 'season', 'week', 'play_type']).size().unstack(fill_value=0).reset_index()

team_data['total_snaps'] = team_data['pass'] + team_data['run']
team_data = team_data.rename(columns={
    'posteam': 'team',
    'pass': 'pass_snaps_count',
    'run': 'rush_snaps_count'
})

team_data['pass_snaps_pct'] = round(team_data.pass_snaps_count / team_data.total_snaps, 2)
team_data['rush_snaps_pct'] = round(team_data.rush_snaps_count / team_data.total_snaps, 2)

sum_data = pbp[pbp.play_type.isin(['run', 'pass'])][[
     'posteam',
     'season',
     'week',
     'touchdown',
     'yards_gained',
     'shotgun',
     'no_huddle',
     'qb_dropback',
     'qb_scramble',
     'pass_length',
     'pass_location',
     'air_yards',
     'yards_after_catch',
     'posteam_score_post',
     'defteam_score_post',
     'score_differential_post',
     'incomplete_pass',
     'interception',
     'fumble_lost',
     'fumble',
     'complete_pass',
     'passer_player_name',
     'passing_yards',
     'receiver_player_id',
     'receiver_player_name',
     'receiving_yards',
     'rusher_player_id',
     'rusher_player_name',
     'rushing_yards',
     'series_result',
     'play_type',
     'play_type_nfl',
     'passer'
]]

print('Getting rushing stats')
rushing_stats = sumData(sum_data, 'run')

print('Getting passing stats')
passing_stats = sumData(sum_data, 'pass')
passing_stats['receiving_td'] = passing_stats.pass_td

print('Getting team stats')
team_stats = sumData(sum_data)
team_stats['pass_attempts'] = team_stats.incomplete_pass + team_stats.complete_pass
team_stats = team_stats.rename(columns={'posteam': 'team'})
team_stats = pd.merge(team_stats, rushing_stats[['team', 'season', 'week', 'run_fumble_lost', 'run_fumble', 'run_td']], on=['team', 'season', 'week'])
team_stats = pd.merge(team_stats, passing_stats[['team', 'season', 'week', 'pass_fumble_lost', 'pass_fumble', 'pass_td', 'receiving_td']], on=['team', 'season', 'week'])
team_stats['yards_gained'] = team_stats.yards_gained + team_stats.receiving_yards

print('Getting points stats')
points = pbp[(pbp.touchdown == 1) | ((pbp.extra_point_attempt == 1) & (pbp.success == 1)) | ((pbp.field_goal_attempt == 1) & (pbp.success == 1))]
points = points.groupby(['posteam', 'season', 'week']).agg({
    'touchdown': 'sum',
    'extra_point_attempt': 'sum',
    'field_goal_attempt': 'sum'
}).reset_index()
points.loc[:, 'td_points'] = points.apply(lambda row: row['touchdown'] * 6, axis=1)
points.loc[:, 'xp_points'] = points.apply(lambda row: row['extra_point_attempt'], axis=1)
points.loc[:, 'fg_points'] = points.apply(lambda row: row['field_goal_attempt'] * 3, axis=1)
points['total_points'] = points['td_points'] + points['xp_points'] + points['fg_points']
points = points.rename(columns={'posteam': 'team'})

print('Getting win-loss stats')
pbp.loc[:, 'winner'] = pbp.apply(lambda row: 'TIE' if row['total_home_score'] == row['total_away_score'] else row['home_team'] if row['total_home_score'] > row['total_away_score'] else row['away_team'], axis=1)
pbp.loc[pbp.play_type_nfl != 'END_GAME', 'winner'] = np.nan
pbp.winner = pbp.winner.fillna(method='bfill')
games = pbp.drop_duplicates(subset='game_id')

away_wins = games.groupby(['away_team', 'season', 'week']).apply(winLossTotal, 'away').reset_index()
away_wins = away_wins.rename(columns={'away_team': 'team'})
home_wins = games.groupby(['home_team', 'season', 'week']).apply(winLossTotal, 'home').reset_index()
home_wins = home_wins.rename(columns={'home_team': 'team'})
wins = pd.concat([home_wins, away_wins]).sort_values(by=['team', 'season', 'week']).fillna(0)

for i in ['wins', 'losses', 'ties']:
    wins.loc[:, i] = 0
    wins.loc[:, i] = wins.apply(lambda row: int(row[f'home_{i}']) + int(row[f'away_{i}']), axis=1)
    wins.loc[:, i] = wins.apply(lambda row: row[i] if row['week'] == 1 else wins[
        (wins.week < row['week']) & (wins.season == row['season']) & (wins.team == row['team'])
    ][i].sum() + (row[f'home_{i}'] + row[f'away_{i}']), axis=1)

wins.loc[:, 'record'] = wins.apply(lambda row: f"{int(row['wins'])}-{int(row['losses'])}-{int(row['ties'])}", axis=1)
wins.loc[:, 'win_pct'] = wins.apply(lambda row: round(row['wins'] / (row['wins']+row['losses']+row['ties']), 3), axis=1)

print('Combining DataFrames')
comb_df = pd.merge(team_data, points, on=['team', 'season', 'week'])
comb_df = pd.merge(comb_df, team_stats, on=['team', 'season', 'week'])
comb_df = pd.merge(comb_df, wins[[
    'team', 'season', 'week', 'wins', 'losses', 'ties', 'win_pct'
]].sort_values(by=['team', 'season', 'week']))
comb_df['receptions'] = comb_df.complete_pass
comb_df['targets'] = comb_df.pass_attempts

comb_df = comb_df[[
    'team', 'season', 'week', 'total_snaps', 'yards_gained', 'touchdown', 'extra_point_attempt', 'field_goal_attempt', 'total_points',
    'td_points', 'xp_points', 'fg_points', 'fumble', 'fumble_lost', 'shotgun', 'no_huddle', 'qb_dropback', 'pass_snaps_count',
    'pass_snaps_pct', 'pass_attempts', 'complete_pass', 'incomplete_pass', 'air_yards', 'passing_yards', 'pass_td', 'interception',
    'targets', 'receptions', 'receiving_yards', 'yards_after_catch', 'receiving_td', 'pass_fumble', 'pass_fumble_lost',
    'rush_snaps_count', 'rush_snaps_pct', 'qb_scramble', 'rushing_yards', 'run_td', 'run_fumble', 'run_fumble_lost', 
    'wins', 'losses', 'ties', 'win_pct'
]]
comb_df.drop_duplicates(inplace=True)
comb_df['yps'] = round(comb_df.yards_gained / comb_df.total_snaps, 2)

data = inputTeamData(comb_df)
NFLTeamStats.objects.bulk_create(data)

print(f"Successfully inserted {len(comb_df)} random records into the NFLTeamStats model!")

# # Teams list for random selection
# teams = [
#     "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN",
#     "DET", "GB", "HOU", "IND", "JAX", "KC", "LV", "LAC", "LAR", "MIA",
#     "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SEA", "SF", "TB",
#     "TEN", "WAS"
# ]

# # Function to generate random data
# def generate_random_data(num_records=10):
#     data = []
#     for _ in range(num_records):
#         data.append(NFLTeamStats(
#             team=random.choice(teams),
#             season=random.randint(2000, 2024),
#             week=random.randint(1, 17),
#             total_snaps=random.randint(50, 80),
#             yards_gained=round(random.uniform(200, 600), 1),
#             touchdown=random.randint(0, 7),
#             extra_point_attempt=random.randint(0, 7),
#             field_goal_attempt=random.randint(0, 7),
#             total_points=round(random.uniform(0, 50), 1),
#             td_points=round(random.uniform(0, 42), 1),
#             xp_points=round(random.uniform(0, 7), 1),
#             fg_points=round(random.uniform(0, 15), 1),
#             fumble=random.randint(0, 5),
#             fumble_lost=random.randint(0, 3),
#             shotgun=random.randint(10, 50),
#             no_huddle=random.randint(0, 10),
#             qb_dropback=random.randint(20, 40),
#             pass_snaps_count=random.randint(30, 50),
#             pass_snaps_pct=round(random.uniform(50, 80), 1),
#             pass_attempts=random.randint(20, 50),
#             complete_pass=random.randint(10, 40),
#             incomplete_pass=random.randint(5, 20),
#             air_yards=round(random.uniform(100, 400), 1),
#             passing_yards=round(random.uniform(100, 500), 1),
#             pass_td=random.randint(0, 5),
#             interception=random.randint(0, 3),
#             targets=random.randint(10, 50),
#             receptions=random.randint(10, 50),
#             receiving_yards=round(random.uniform(50, 300), 1),
#             yards_after_catch=round(random.uniform(10, 150), 1),
#             receiving_td=random.randint(0, 3),
#             pass_fumble=random.randint(0, 2),
#             pass_fumble_lost=random.randint(0, 2),
#             rush_snaps_count=random.randint(10, 50),
#             rush_snaps_pct=round(random.uniform(20, 50), 1),
#             qb_scramble=random.randint(0, 5),
#             rushing_yards=round(random.uniform(50, 300), 1),
#             run_td=random.randint(0, 3),
#             run_fumble=random.randint(0, 2),
#             run_fumble_lost=random.randint(0, 2),
#             home_wins=random.randint(0, 8),
#             home_losses=random.randint(0, 8),
#             home_ties=random.randint(0, 1),
#             away_wins=random.randint(0, 8),
#             away_losses=random.randint(0, 8),
#             away_ties=random.randint(0, 1),
#             wins=random.randint(0, 16),
#             losses=random.randint(0, 16),
#             ties=random.randint(0, 1),
#             win_pct=round(random.uniform(0, 1), 3),
#             record=f"{random.randint(0, 16)}-{random.randint(0, 16)}-{random.randint(0, 1)}",
#             yps=round(random.uniform(4, 8), 2)
#         ))
#     return data

# # Generate random data and insert it into the database
# num_records = 10  # Adjust the number of records as needed
# random_data = generate_random_data(num_records)
# NFLTeamStats.objects.bulk_create(random_data)

# print(f"Successfully inserted {num_records} random records into the NFLTeamStats model!")