import os
import django
import nfl_data_py as nfl
import pandas as pd
import concurrent.futures
import time
import numpy as np
import warnings
from team_stats_add import importData
warnings.filterwarnings('ignore')

print('Getting environment details')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from stats.models import NFLPlayerStats

def getFantasyPoints(row):
    td_points = (row['run_td']+row['reception_td']+row['pass_td'])*6
    pass_yards_points = row['passing_yards']*0.04
    other_yards_points = (row['rushing_yards']+row['receiving_yards'])*0.1
    fumble = (row['run_fumble_lost'] + row['pass_fumble_lost'] + row['reception_fumble_lost'])*3
    total_points = (td_points + pass_yards_points + other_yards_points + row['receptions']) - (row['interception']*2 + fumble)
    return round(total_points, 2)

def sumData(i, df):
    data_dict = {
                    'yards_gained': 'sum',
                    'touchdown': 'sum',
                    'fumble_lost': 'sum'
                }

    if i.upper() == 'RUN':
        pass
    elif i.upper() == 'PASS':
        for stat in ['air_yards', 'incomplete_pass', 'interception', 'complete_pass']:
            data_dict[stat] = 'sum'
    else:
        for stat in ['air_yards', 'complete_pass', 'yards_after_catch']:
            data_dict[stat] = 'sum'
    
    if i == 'reception':
        new_df = df[df.play_type == 'pass'].groupby(['receiver_player_id', 'season', 'week', 'play_type']).agg(data_dict).unstack(fill_value=0).reset_index()
    elif i == 'run':
        new_df = df[df.play_type == 'run'].groupby(['rusher_player_id', 'season', 'week', 'play_type']).agg(data_dict).unstack(fill_value=0).reset_index()
    else:
        new_df = df[df.play_type == 'pass'].groupby(['passer_player_id', 'season', 'week', 'play_type']).agg(data_dict).unstack(fill_value=0).reset_index()
    new_df.columns = [i[0] for i in new_df.columns]
    new_df = new_df.rename(columns={'fumble_lost':f'{i}_fumble_lost', 'fumble':f'{i}_fumble', 'touchdown':f'{i}_td'})

    return new_df
    
def get_pr(row):
    if row['pass_attempts'] == 0:
        return 0
    a = ((row['complete_pass']/row['pass_attempts'])-0.3)*5
    b = ((row['passing_yards']/row['pass_attempts'])-3)*0.25
    c = (row['pass_td']/row['pass_attempts'])*20
    d = 2.375-((row['interception']/row['pass_attempts'])*25)
    pr = round(((a+b+c+d)/6)*100, 2)
    if pr > 158.3:
        pr = 158.3
    return pr

def getTempId(df, row, count=0):
    name_split = row['player_name'].replace('.', '').split(' ')
    temp_id = name_split[1][:3] + name_split[0][:3] + f'{count}'
    if len(df[df.temp_player_id == temp_id]) > 0:
        count += 1
        temp_id = temp_id[:-1] + f'{count}'
    return temp_id

print('Getting play-by-play data')
pbp = importData('pbp', [2012, 2023])
pbp = pbp[pbp.season_type == 'REG']
pbp.game_date = pd.to_datetime(pbp.game_date)
pbp = pbp[pbp.play_type.isin(['run', 'pass'])].sort_values(by=['season'])

print('Getting rush, receiving, and passing data')
rush_data = pbp[pbp.play_type == 'run'].groupby([
    'rusher_player_id', 'season', 'week', 'play_type'
]).size().unstack(fill_value=0).reset_index()
rush_data = rush_data.rename(columns={
    'run': 'rush_attempts', 'rusher_player_id': 'player_id'
})

pass_data = pbp[pbp.play_type == 'pass'].groupby([
    'passer_player_id', 'season', 'week', 'play_type'
]).size().unstack(fill_value=0).reset_index()
pass_data = pass_data.rename(columns={
    'pass': 'pass_attempts', 'passer_player_id': 'player_id'
})

rec_data = pbp[pbp.play_type == 'pass'].groupby([
    'receiver_player_id', 'season', 'week', 'play_type'
]).size().unstack(fill_value=0).reset_index()
rec_data = rec_data.rename(columns={
    'pass': 'targets', 'receiver_player_id': 'player_id'
})

sum_data = pbp[pbp.play_type.isin(['run', 'pass'])][[
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
     'passer_player_id',
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

print('Summing data')
rushing_stats = sumData('run', sum_data)
rushing_stats = rushing_stats.rename(columns={
    'yards_gained': 'rushing_yards',
    'rusher_player_id': 'player_id'
})
rushing_stats = pd.merge(rushing_stats, rush_data, on=['season', 'week', 'player_id'])

pass_stats = sumData('pass', sum_data)
pass_stats = pass_stats.rename(columns={
    'yards_gained': 'passing_yards', 'air_yards': 'passing_air_yards', 'passer_player_id': 'player_id'
})
pass_stats = pd.merge(pass_stats, pass_data, on=['season', 'week', 'player_id'])

rec_stats = sumData('reception', sum_data)
rec_stats = rec_stats.rename(columns={
    'yards_gained': 'receiving_yards', 'air_yards': 'receiving_air_yards', 'complete_pass': 'receptions',
    'receiver_player_id': 'player_id'
})
rec_stats = pd.merge(rec_stats, rec_data, on=['player_id', 'season', 'week'])

print('Combining DataFrames')
joined_rush = rushing_stats.set_index(['player_id', 'season', 'week']).join(rec_stats.set_index(['player_id', 'season', 'week'])).join(pass_stats.set_index(['player_id', 'season', 'week'])).reset_index()
joined_rec = rec_stats.set_index(['player_id', 'season', 'week']).join(rushing_stats.set_index(['player_id', 'season', 'week'])).join(pass_stats.set_index(['player_id', 'season', 'week'])).reset_index()
joined_pass = pass_stats.set_index(['player_id', 'season', 'week']).join(rushing_stats.set_index(['player_id', 'season', 'week'])).join(rec_stats.set_index(['player_id', 'season', 'week'])).reset_index()

comb_df = pd.concat([joined_rush, joined_rec, joined_pass])
comb_df.fillna(0).drop_duplicates(inplace=True)

print('Getting fantasy points')
fantasy_points = comb_df.groupby(['season', 'week', 'player_id']).apply(getFantasyPoints).reset_index()
fantasy_points = fantasy_points.drop('level_3', axis=1).rename(columns={0: 'fantasy_points_ppr'})

comb_df = pd.merge(comb_df, fantasy_points, on=['season', 'week', 'player_id'])

print('Getting depth charts')
dc = importData('depth charts', [2012, 2023])
dc = dc[dc.position.isin([
    'QB', 'RB', 'WR', 'TE'
])]
dc = dc[[
    'season', 'week', 'club_code', 'game_type', 'depth_team', 'full_name', 'gsis_id', 'position'
]].rename(columns={
    'club_code': 'team',
    'full_name': 'player_name',
    'gsis_id': 'player_id'
})
dc.depth_team = dc.depth_team.astype(int)
dc = dc[dc.game_type == 'REG']

depth = dc[['season', 'week', 'player_id', 'depth_team']].groupby(['season', 'week', 'player_id']).agg({'depth_team': 'mean'}).round().reset_index()

x = dc.groupby([
    'season', 'week', 'player_id', 'player_name', 'position', 'team'
]).agg({'team': 'count'}).rename(columns={'team': 'count'}).reset_index()

same_teams = x[x.duplicated(subset=['season', 'week', 'player_id', 'player_name', 'position']) == False]

new_teams = x[x.duplicated(subset=['season', 'week', 'player_id', 'player_name', 'position'], keep=False)]
new_teams = new_teams.sort_values(by=['season', 'week', 'player_name', 'count'], ascending=False).drop_duplicates(subset=[
    'season', 'week', 'player_name', 'position'
])

print('Assigning depth')
dc = pd.concat([same_teams, new_teams]).drop_duplicates(subset=['season', 'week', 'player_id'], keep='last')
dc = pd.merge(dc, depth, on=['season', 'week', 'player_id'], how='left').rename(columns={'depth_team': 'depth'})
dc.loc[dc.team == 'STL', 'team'] = 'LA'
dc.loc[dc.team == 'SD', 'team'] = 'LAC'
dc.loc[dc.team == 'OAK', 'team'] = 'LV'

comb_df = pd.merge(comb_df, dc, on=['player_id', 'season', 'week'], how='left').drop_duplicates()
comb_df = comb_df[comb_df.position.isin(['QB', 'RB', 'WR', 'TE'])]
comb_df = comb_df[[
    'team', 'player_id', 'player_name', 'position', 'season', 'week', 'depth', 'pass_attempts', 'complete_pass', 
    'incomplete_pass', 'passing_yards', 'passing_air_yards', 'pass_td', 'interception', 'pass_fumble_lost', 'targets',
    'receptions', 'receiving_yards', 'receiving_air_yards', 'yards_after_catch', 'reception_td', 'reception_fumble_lost',
    'rush_attempts', 'rushing_yards', 'run_td', 'run_fumble_lost', 'fantasy_points_ppr'
]]

print('Creating additional features')
air_yards = comb_df.groupby(['team', 'season', 'week']).agg({'passing_air_yards': 'sum'}).reset_index()

attempts = comb_df.groupby(['team', 'season', 'week']).agg({'pass_attempts': 'sum'}).reset_index()

comb_df['adot'] = round(comb_df.receiving_air_yards / comb_df.targets, 3)

comb_df.loc[:, 'air_yards_share'] = comb_df.apply(lambda row: abs(round(row['receiving_air_yards'] / air_yards[air_yards.team == row['team']].passing_air_yards.values[0], 3)), axis=1)
comb_df.loc[:, 'target_share'] = comb_df.apply(lambda row: abs(round(row['targets']/attempts[attempts.team==row['team']].pass_attempts.values[0], 3)), axis=1)

comb_df['comp_pct'] = round(comb_df.complete_pass/comb_df.pass_attempts, 3)
comb_df['int_pct'] = round(comb_df.interception/comb_df.pass_attempts, 3)
comb_df['pass_td_pct'] = round(comb_df.pass_td/comb_df.pass_attempts, 3)
comb_df['ypa'] = round(comb_df.passing_yards/comb_df.pass_attempts, 2)
comb_df['rec_td_pct'] = round(comb_df.reception_td/comb_df.targets, 3)
comb_df['yptarget'] = round(comb_df.receiving_yards/comb_df.targets, 2)
comb_df['ypr'] = round(comb_df.receiving_yards/comb_df.receptions, 2)
comb_df['rush_td_pct'] = round(comb_df.run_td/comb_df.rush_attempts, 3)
comb_df['ypc'] = round(comb_df.rushing_yards/comb_df.rush_attempts, 2)
comb_df['touches'] = sum([comb_df.pass_attempts, comb_df.receptions, comb_df.rush_attempts])
comb_df['total_tds'] = sum([comb_df.run_td, comb_df.pass_td, comb_df.reception_td])
comb_df['td_pct'] = round(comb_df.total_tds/comb_df.touches, 2)
comb_df['total_yards'] = sum([comb_df.passing_yards, comb_df.receiving_yards, comb_df.rushing_yards])
comb_df['yptouch'] = round(comb_df.total_yards/comb_df.touches, 2)
comb_df = comb_df.fillna(0)

print('Getting passer rating')
comb_df['passer_rating'] = comb_df.apply(lambda row: get_pr(row), axis=1)

print('Assigning temporary ids')
comb_df['temp_player_id'] = ''
comb_df.loc[:, 'temp_player_id'] = comb_df.apply(lambda row: getTempId(comb_df, row), axis=1)

print('Getting snaps data')
snaps = importData('snaps', [2012, 2023])
snaps = snaps.drop([
    'game_id', 'pfr_game_id', 'pfr_player_id', 'defense_snaps', 'defense_pct', 'st_snaps', 'st_pct'
], axis=1)

snaps = snaps[(snaps.game_type=='REG')&(snaps.position.isin([
    'QB', 'WR', 'RB', 'TE'
]))].rename(columns={
    'player': 'player_name'
})
snaps = snaps[snaps.offense_snaps != 0]

temp = snaps.copy()
temp.drop_duplicates(subset=['season', 'week', 'player_name', 'position'], inplace=True)
temp['temp_player_id'] = ''
temp.loc[:, 'temp_player_id'] = temp.apply(lambda row: getTempId(temp, row), axis=1)
snaps = pd.merge(snaps, temp.drop([i for i in temp.columns if i not in ['season', 'week', 'player_name', 'position', 'temp_player_id']], axis=1), on=['season', 'week', 'player_name', 'position'], how='left')

snaps = snaps.groupby(['season', 'week', 'game_type', 'player_name', 'team', 'position', 'temp_player_id']).agg({
    'offense_pct': 'mean'
}).reset_index().sort_values(by=['week', 'season', 'player_name'])

snaps.offense_pct = round(snaps.offense_pct, 3)

snaps.loc[:, 'temp_player_id'] = snaps.apply(lambda row: row['temp_player_id'].replace('.', ''), axis=1)

print('Getting player data')
ids = importData('ids', [2012, 2023])
ids.loc[:, 'birth_year'] = ids.apply(lambda row: row['birthdate'] if type(row['birthdate']) == float else row['birthdate'].split('-')[0], axis=1)
ids = ids[[
    'gsis_id', 'birth_year', 'draft_year', 'draft_round', 'draft_pick', 'draft_ovr', 'height', 'weight', 'college'
]][(ids.gsis_id.notna()) & (ids.position.isin(['QB', 'RB', 'WR', 'TE']))].rename(columns={'gsis_id': 'player_id'})

comb_df = pd.merge(comb_df, ids, on='player_id')
comb_df.loc[:, 'age'] = comb_df.season.astype(int) - comb_df.birth_year.astype(int)
comb_df.drop('birth_year', axis=1, inplace=True)

print(len(comb_df.columns))
print(len(comb_df))

print(comb_df.sort_values(by=['player_name', 'season', 'week']))