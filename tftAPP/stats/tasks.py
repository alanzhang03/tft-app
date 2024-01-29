from tftAPP.celery import app
import requests
import pandas as pd
import numpy as np
import time
from django.db import models

@app.task
def task_one():
    api_key = 'RGAPI-ef9072cf-f04c-4de4-af57-dc275ffb68de'

    ## get the puuids of the top 250 players in north america


    api_url = 'https://na1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT'
    api_url = api_url + '&api_key=' + api_key
    challenger_players_response = requests.get(api_url).json()
    challenger_summoner_ids = [challenger_players_response['entries'][i]['summonerId'] for i in range(0, len(challenger_players_response['entries']))]
    challenger_puuids = []

    count = 1
    for id in challenger_summoner_ids:
        summoner_url = 'https://na1.api.riotgames.com/tft/summoner/v1/summoners/'+ id + '?api_key=' + api_key
        ## delete when have production key
        if count % 100 == 0:
            time.sleep(120)
            print("sleeping 120s")
        r = requests.get(summoner_url).json()
        challenger_puuids.append(r['puuid'])
        count += 1


    ## get a list of all match ids within the last hour
    import time
    recent_match_ids = []
    start_time = int(time.time()) - 3600

    ##
    count = 1
    for puuid in challenger_puuids:
        api_url_matches = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?start=0&startTime=' + str(start_time) + '&count=20&api_key=' + api_key
        r = requests.get(api_url_matches).json()
        recent_match_ids = list(set(recent_match_ids + r))

        ## delete when have production key
        if count % 100 == 0:
            time.sleep(120)
            print("sleeping 120s")
        count += 1

    ## add data to database
    augments = pd.DataFrame(columns=['2-1 Games', '2-1 Avg Placement', '3-2 Games', '3-2 Avg Placement', '4-2 Games', '4-2 Avg Placement', 'Total Games', 'Total Avg Placement'])
    augments = augments.astype({
        '2-1 Games':int,
        '2-1 Avg Placement':float,
        '3-2 Games':int,
        '3-2 Avg Placement':float,
        '4-2 Games':int,
        '4-2 Avg Placement':float,
        'Total Games':int,
        'Total Avg Placement':float,
        })

    data_dragon = requests.get('https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/tft-augments.json').json()
    aug_ids = list(data_dragon['data'].keys())
    aug_names = [data_dragon['data'][i]['name'] for i in list(data_dragon['data'].keys())]

    augments.insert(0, "Augment ID", aug_ids)
    augments.insert(0, "Augment Name", aug_names)

    augments['2-1 Games'] = 0
    augments['3-2 Games'] = 0
    augments['4-2 Games'] = 0
    augments['Total Games'] = 0


    count = 1
    for match_id in recent_match_ids:

        if count % 100 == 0:
            time.sleep(120)
            print("sleeping 120s")

        api_url = 'https://americas.api.riotgames.com/tft/match/v1/matches/'+ match_id + '?api_key=' + api_key
        r = requests.get(api_url).json()
        for i in range(0, 8):
            # add to database
            ags = ['', '', '']
            augs = r['info']['participants'][i]['augments']
            for i in range(0, len(augs)):
                ags[i] = augs[i]
            placement = r['info']['participants'][i]['placement']


            if ags[0] != '':
                avg_place_21 = augments.loc[augments['Augment ID'] == ags[0], '2-1 Avg Placement'].values[0]
                games_21 = augments.loc[augments['Augment ID'] == ags[0], '2-1 Games'].values[0]
                avg_total_place_21 = augments.loc[augments['Augment ID'] == ags[0], 'Total Avg Placement'].values[0]
                games_total_21 = augments.loc[augments['Augment ID'] == ags[0], 'Total Games'].values[0]


                if pd.isna(avg_place_21):
                    augments.loc[augments['Augment ID'] == ags[0], '2-1 Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[0], '2-1 Avg Placement'] = ((avg_place_21 * games_21) + placement) / (games_21 + 1)

                if pd.isna(avg_total_place_21):
                    augments.loc[augments['Augment ID'] == ags[0], 'Total Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[0], 'Total Avg Placement'] = ((avg_total_place_21 * games_total_21) + placement) / (games_total_21 + 1)

                augments.loc[augments['Augment ID'] == ags[0], '2-1 Games'] += 1
                augments.loc[augments['Augment ID'] == ags[0], 'Total Games'] += 1

            if ags[1] != '':
                avg_place_32 = augments.loc[augments['Augment ID'] == ags[1], '3-2 Avg Placement'].values[0]
                games_32 = augments.loc[augments['Augment ID'] == ags[1], '3-2 Games'].values[0]
                avg_total_place_32 = augments.loc[augments['Augment ID'] == ags[1], 'Total Avg Placement'].values[0]
                games_total_32 = augments.loc[augments['Augment ID'] == ags[1], 'Total Games'].values[0]

                if pd.isna(avg_place_32):
                    augments.loc[augments['Augment ID'] == ags[1], '3-2 Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[1], '3-2 Avg Placement'] = ((avg_place_32 * games_32) + placement) / (games_32 + 1)
                if pd.isna(avg_total_place_32):
                    augments.loc[augments['Augment ID'] == ags[1], 'Total Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[1], 'Total Avg Placement'] = ((avg_total_place_32 * games_total_32) + placement) / (games_total_32 + 1)

                augments.loc[augments['Augment ID'] == ags[1], '3-2 Games'] += 1
                augments.loc[augments['Augment ID'] == ags[1], 'Total Games'] += 1



            if ags[2] != '':
                avg_place_42 = augments.loc[augments['Augment ID'] == ags[2], '4-2 Avg Placement'].values[0]
                games_42 = augments.loc[augments['Augment ID'] == ags[2], '4-2 Games'].values[0]
                avg_total_place_42 = augments.loc[augments['Augment ID'] == ags[2], 'Total Avg Placement'].values[0]
                games_total_42 = augments.loc[augments['Augment ID'] == ags[2], 'Total Games'].values[0]

                if pd.isna(avg_place_42):
                    augments.loc[augments['Augment ID'] == ags[2], '4-2 Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[2], '4-2 Avg Placement'] = ((avg_place_42 * games_42) + placement) / (games_42 + 1)
                if pd.isna(avg_total_place_42):
                    augments.loc[augments['Augment ID'] == ags[2], 'Total Avg Placement'] = float(placement)
                else:
                    augments.loc[augments['Augment ID'] == ags[2], 'Total Avg Placement'] = ((avg_total_place_42 * games_total_42) + placement) / (games_total_42 + 1)

                augments.loc[augments['Augment ID'] == ags[2], '4-2 Games'] += 1
                augments.loc[augments['Augment ID'] == ags[2], 'Total Games'] += 1

        count += 1



    # updating database
    import os
    import sys
    sys.path.append('..')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tftAPP.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    import django
    django.setup()
    from stats.models import Augment



    for row in augments.iterrows():
        # print(row[1])

        new_games_total = row[1]['Total Games']
        new_games_two_one = row[1]['2-1 Games']
        new_games_three_two = row[1]['3-2 Games']
        new_games_four_two = row[1]['4-2 Games']

        new_avg_total = row[1]['Total Avg Placement']
        new_avg_total = 0.0 if pd.isna(new_avg_total) else new_avg_total
        new_avg_two_one = row[1]['2-1 Avg Placement']
        new_avg_two_one = 0.0 if pd.isna(new_avg_two_one) else new_avg_two_one
        new_avg_three_two = row[1]['3-2 Avg Placement']
        new_avg_three_two = 0.0 if pd.isna(new_avg_three_two) else new_avg_three_two
        new_avg_four_two = row[1]['4-2 Avg Placement']
        new_avg_four_two = 0.0 if pd.isna(new_avg_four_two) else new_avg_four_two

        prevaug = Augment.objects.get(name=row[1]['Augment Name'])

        games_total = prevaug.games_total
        games_two_one = prevaug.games_two_one
        games_three_two = prevaug.games_three_two
        games_four_two = prevaug.games_four_two

        avg_total = float(prevaug.avg_total)
        avg_two_one = float(prevaug.avg_two_one)
        avg_three_two = float(prevaug.avg_three_two)
        avg_four_two = float(prevaug.avg_four_two)

        avg_total = 0.0 if new_games_total + games_total == 0 else ((avg_total * games_total) + (new_avg_total * new_games_total)) / (new_games_total + games_total)
        avg_two_one = 0.0 if new_games_two_one + games_two_one == 0 else ((avg_two_one * games_two_one) + (new_avg_two_one * new_games_two_one)) / (new_games_two_one + games_two_one)
        avg_three_two = 0.0 if new_games_three_two + games_three_two == 0 else ((avg_three_two * games_three_two) + (new_avg_three_two * new_games_three_two)) / (new_games_three_two + games_three_two)
        avg_four_two = 0.0 if new_games_four_two + games_four_two == 0 else ((avg_four_two * games_four_two) + (new_avg_four_two * new_games_four_two)) / (new_games_four_two + games_four_two)

        games_total += new_games_total
        games_two_one += new_games_two_one
        games_three_two += new_games_three_two
        games_four_two += new_games_four_two


        Augment.objects.filter(name=row[1]['Augment Name']).update(games_total=games_total,
                                                                games_two_one=games_two_one,
                                                                games_three_two=games_three_two,
                                                                games_four_two=games_four_two,
                                                                avg_total=avg_total,
                                                                avg_two_one=avg_two_one,
                                                                avg_three_two=avg_three_two,
                                                                avg_four_two=avg_four_two)


        # aug = Augment(name = row[1]['Augment Name'], 
        #               games_total = new_games_total, 
        #               games_two_one = new_games_two_one,
        #               games_three_two = new_games_three_two,
        #               games_four_two = new_games_four_two,
        #               avg_total = 0.0 if pd.isna(new_avg_total) else new_avg_total,
        #               avg_two_one = 0.0 if pd.isna(new_avg_two_one) else new_avg_two_one,
        #               avg_three_two = 0.0 if pd.isna(new_avg_three_two) else new_avg_three_two,
        #               avg_four_two = 0.0 if pd.isna(new_avg_four_two) else new_avg_four_two)
        # aug.save()
    return "success"