import pandas as pd
from pybaseball import pitching_stats, batting_stats, statcast
import matplotlib.pyplot as plt
import numpy as np
import requests
from tqdm import tqdm
from datetime import datetime


# def run_pitchers(year_start, year_end):
#     data = pitching_stats(year_start, year_end, qual=1)
#     # df = data.groupby('Name').sum()
#     df = data.sort_values(by=['Pitches'], ascending=False)
#     df.to_excel('pitches.xlsx')
#     most_pitches = df[['Pitches', 'Strikes', 'Balls', 'Relief-IP']].copy()
#     most_pitches = most_pitches.rename(columns={"Relief-IP": "Relief_Innings"})
#     most_pitches['Strikes_per_Pitch'] = most_pitches['Strikes'] / most_pitches['Pitches']
#     most_pitches['Pitches/Yr'] = most_pitches['Pitches']/(year_end - year_start)
#     most_pitches = most_pitches[most_pitches.Relief_Innings >= 200]
#     most_pitches = most_pitches[most_pitches.Pitches >= 4000]
#
#     fig, ax = plt.subplots()
#     people = most_pitches.index
#     y_pos = np.arange(len(people))
#     pitches = most_pitches['Pitches']
#
#     ax.barh(y_pos, pitches, align='center')
#     ax.set_yticks(y_pos, labels=people)
#     ax.invert_yaxis()
#     ax.set_xlabel('pitches')
#     ax.set_title('2017-2022 MLB Relief Pitchers Total Pitches (200+ innings pitched)')
#
#     plt.show()
#
#     most_pitches = most_pitches.sort_values(by='Pitches/Yr')
#     return most_pitches
#
#
# def run_batters(year):
#     batters = batting_stats(year, qual=1)
#     hard_hit = batters.sort_values(by=['HardHit'], ascending=False)
#     df = hard_hit.groupby('Team').sum()
#     plt.bar(df.index, df['HardHit'], color=plt.cm.Paired(np.arange(len(df))))
#     plt.show()
#     return df

def find_video(pitch):
    pitch_map = {
        "Inning": int(pitch['inning']),
        "pitcher_id": pitch['pitcher'],
        "batter_id": pitch['batter'],
        "game_pk": str(pitch['game_pk']),
        "balls": int(pitch['balls']),
        "strikes": int(pitch['strikes']),
        "outs": int(pitch['outs_when_up']),
        "pitch_number": int(pitch['pitch_number'])
    }

    try:

        gm_pk = pitch['game_pk']
        url = "https://baseballsavant.mlb.com/gf?game_pk={GAME_PK}".replace('{GAME_PK}', str(gm_pk))
        resp = requests.get(url)
        response = resp.json()

        found = False
        play_id = '0000'
        if not found:
            for i in response['team_away']:
                if i['inning'] == pitch_map['Inning'] and i['pitcher'] == pitch_map['pitcher_id'] and i['batter'] == pitch_map['batter_id'] and i['game_pk'] == pitch_map['game_pk']:

                    if i['pitch_number'] == pitch_map['pitch_number']:
                        play_id = i['play_id']

        if not found:
            for i in response['team_home']:

                if i['inning'] == pitch_map['Inning'] and i['pitcher'] == pitch_map['pitcher_id'] and i['batter'] == pitch_map['batter_id'] and i['game_pk'] == pitch_map['game_pk']:

                    if i['pitch_number'] == pitch_map['pitch_number']:
                        play_id = i['play_id']

        url = "https://baseballsavant.mlb.com/sporty-videos?playId={PLAY_ID}".replace("{PLAY_ID}", str(play_id))
        return url

    except Exception as e:
        print(e)
        pass


def run_statcast(team):
    data = statcast('2022-05-26', '2022-05-27', team=team)
    links = []
    for index, value in tqdm(data.iterrows(), total=data.shape[0]):
        link = find_video(value)
        links.append(link)
        # if index == 10:
        #     break
        # else:
        continue
    links = pd.Series(links)
    data['url'] = links

    data.to_excel('NYY_5_27_22.xlsx')


# run_pitchers(2021, 2022)
# # run_batters(2022)

if __name__ == '__main__':
    run_statcast('NYY')
