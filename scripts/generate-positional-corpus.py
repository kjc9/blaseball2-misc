#!bin/python3

import json
import csv
import re

game_list = "../data/s1/games-list.txt"
player_file = "../data/s1/players/processed_players.csv"
with open(game_list, "r") as read_file:
    lines = read_file.readlines()
files = []
for line in lines:
    line = line.replace("\n", "")
    files.append(line)

coord_map = {}
for x in range(0,6):
    for y in range(0,6):
        key = f'{x}-{y}'
        print(f"opening |{key}|...")
        coord_map[key] = open(f"../data/s1/corpora/coords/{key}.txt", "w")

SINGLE = "SINGLE"
DOUBLE = "DOUBLE"
TRIPLE = "TRIPLE"
HOME_RUN = "HOME_RUN"
FIELDERS_CHOICE = "FIELDERS_CHOICE"
FLYOUT = "FLY_OUT"
GROUNDOUT = "GROUND_OUT"

def handle_hit(cur_pitcher, cur_batter, named_defender, display_str):
    key = f'{player_x[named_defender]}-{player_y[named_defender]}'
    HANDLE = coord_map[key]
    HANDLE.write(f'HIT,{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')
    if "Single" in display_str:
        HANDLE.write(f'{SINGLE},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')
    elif "Double" in display_str:
        HANDLE.write(f'{DOUBLE},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')
    elif "Triple" in display_str:
        HANDLE.write(f'{TRIPLE},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')
    elif "Home Run" in display_str:
        HANDLE.write(f'{HOME_RUN},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')

def handle_flyout(cur_pitcher, cur_batter, named_defender):
    key = f'{player_x[named_defender]}-{player_y[named_defender]}'
    HANDLE = coord_map[key]
    HANDLE.write(f'{FLYOUT},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')

def handle_groundout(cur_pitcher, cur_batter, named_defender, display_str):
    key = f'{player_x[named_defender]}-{player_y[named_defender]}'
    HANDLE = coord_map[key]
    HANDLE.write(f'{GROUNDOUT},{heat_map[cur_batter]},{heat_map[cur_pitcher]}\n')

feature_map = {}
heat_map = {}
player_x = {}
player_y = {}
zero_fv = []
for x in range(0, 100):
    zero_fv.append("0")
with open(player_file, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        id = row[1]
        player_x[id] = row[6]
        player_y[id] = row[7]
        feature_map[id] = ",".join(row[6:59])
        heat_map[id] = ",".join(row[23:59])
        #print(f'{row[2]} == |{feature_map[id]}|')
    feature_map["0"] = ",".join(zero_fv[6:59])


#files = ["ffcc18e6-5304-4567-9977-68e0e30371df.json"]

for file in files:
    cur_batter = ""
    cur_pitcher = ""
    named_defender = ""
    cur_def_arr = []
    cur_def_name = {}
    cur_runner_arr = []
    print(f'WORKING on {file}')
    with open(f'../data/s1/games/{file}', "r") as json_file:
        cur_game = json.load(json_file)
        for event in cur_game:
            if 'batter' in event['data']['changedState'] and \
                    'pitcher' in event['data']['changedState'] and \
                    'defenders' in event['data']['changedState']:
                # update the cur batter, pitcher and defender pattern
                if event['data']['changedState']['batter'] != None:
                    cur_batter = event['data']['changedState']['batter']['id']

                if event['data']['changedState']['pitcher'] != None:
                    cur_pitcher = event['data']['changedState']['pitcher']['id']
                cur_def_arr = []
                cur_def_name = {}
                for defender in event['data']['changedState']['defenders']:
                    if defender['name'].startswith('DeAndre') and defender['name'].endswith('Possum'):
                        defender['name'] = "DeAndre OPossum"
                    if defender['name'].startswith('Carter') and defender['name'].endswith('connor'):
                        defender['name'] = "Carter Oconnor"
                    cur_def_name[defender['name']] = defender['id']
                    cur_def_arr.append(defender['id'])
            if 'baserunners' in event['data']['changedState']:
                #cur_runner_arr = []
                for runner in event['data']['changedState']['baserunners']:
                    cur_runner_arr.append(runner['id'])

            display_str = event['data']['displayText']
            display_str = display_str.replace('Carter O&#x27;connor', 'Carter Oconnor').replace('DeAndre O&#x27;Possum', 'DeAndre OPossum')
            for defender in cur_def_name:
                if defender in display_str:
                    named_defender = cur_def_name[defender]

            if display_str == 'Play Ball!' or display_str.startswith("End of the"):
                continue
            if cur_batter == '':
                print("EMPTY BATTER")
                continue

            if cur_pitcher == '':
                print("EMPTY PITCHER")
                continue

            if named_defender == '':
                print("EMPTY DEFENDER")
                continue

            if "Single" in display_str or "Double" in display_str or "Triple" in display_str:
                handle_hit(cur_pitcher, cur_batter, named_defender, display_str)

            if " makes" in display_str or "to make" in display_str or "ly out" in display_str:
                handle_flyout(cur_pitcher, cur_batter, named_defender)

            if "roundout" in display_str or "forced out" in display_str:
                handle_groundout(cur_pitcher, cur_batter, named_defender, display_str)
