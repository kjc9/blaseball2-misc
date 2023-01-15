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

STRIKE_GENERIC = "STRIKE_GENERIC"
STRIKE_LOOKING = "STRIKE_LOOKING"
STRIKE_SWINGING = "STRIKE_SWINGING"
BALL_GENERIC = "BALL_GENERIC"
BALL_QUALITY = "BALL_QUALITY"
BALL_MISS = "BALL_MISS"
FOUL = "FOUL"
SINGLE = "SINGLE"
DOUBLE = "DOUBLE"
TRIPLE = "TRIPLE"
HOME_RUN = "HOME_RUN"
FIELDERS_CHOICE = "FIELDERS_CHOICE"
FLYOUT = "FLY_OUT"
GROUNDOUT = "GROUND_OUT"

## Primary files
BALL_GENERIC_FILE = open("../data/s1/corpora/ball_generic_data.txt", "w")
BALL_QUALITY_FILE = open("../data/s1/corpora/ball_quality_data.txt", "w")
BALL_MISS_FILE = open("../data/s1/corpora/ball_miss_data.txt", "w")
STRIKE_FILE = open("../data/s1/corpora/strike_data.txt", "w")
STRIKE_LOOKING_FILE = open("../data/s1/corpora/strike_looking_data.txt", "w")
STRIKE_SWINGING_FILE = open("../data/s1/corpora/strike_swinging_data.txt", "w")
FOUL_FILE = open("../data/s1/corpora/foul_data.txt", "w")
CONTACT_OUT_FILE = open("../data/s1/corpora/contact_out_data.txt", "w")
CONTACT_HIT_FILE = open("../data/s1/corpora/contact_hit_data.txt", "w")

## Secondary files
STRIKEOUT_FILE = open("../data/s1/corpora/ab/strikeout_data.txt", "w")
#FIELDOUT_FILE = open("../data/s1/corpora/ab/fieldout_data.txt", "w")
FLYOUT_FILE = open("../data/s1/corpora/ab/flyout_data.txt", "w")
GROUNDOUT_FILE = open("../data/s1/corpora/ab/groundout_data.txt", "w")
WALK_FILE = open("../data/s1/corpora/ab/walk_data.txt", "w")
SINGLE_FILE = open("../data/s1/corpora/ab/single_data.txt", "w")
DOUBLE_FILE = open("../data/s1/corpora/ab/double_data.txt", "w")
TRIPLE_FILE = open("../data/s1/corpora/ab/triple_data.txt", "w")
HR_FILE = open("../data/s1/corpora/ab/hr_data.txt", "w")
FC_FILE = open("../data/s1/corpora/ab/fc_data.txt", "a")
#SAC_FILE = open("../ab/sac_data.txt", "a")

def handle_ball(cur_pitcher, cur_batter, display_str):
    if " walk" in display_str:
        WALK_FILE.write(f'WALK,{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    if "big time" in display_str or "way outside" in display_str or "extremely outside" in display_str:
        BALL_MISS_FILE.write(f'{BALL_MISS},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    elif "just " in display_str:
        BALL_QUALITY_FILE.write(f'{BALL_QUALITY},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    else:
        BALL_GENERIC_FILE.write(f'{BALL_GENERIC},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')

def handle_strike(cur_pitcher, cur_batter, display_str):
    if "trikes " in display_str:
        STRIKEOUT_FILE.write(f'STRIKEOUT,{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    if " looking" in display_str:
        STRIKE_LOOKING_FILE.write(f'{STRIKE_LOOKING},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    elif " swinging" in display_str:
        STRIKE_SWINGING_FILE.write(f'{STRIKE_SWINGING},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')
    else:
        STRIKE_FILE.write(f'{STRIKE_GENERIC},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')

def handle_foul(cur_pitcher, cur_batter):
    FOUL_FILE.write(f'{FOUL},{feature_map[cur_batter]},{feature_map[cur_pitcher]}\n')

def handle_hit(cur_pitcher, cur_batter, named_defender, display_str):
    CONTACT_HIT_FILE.write(f'HIT,{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    if "Single" in display_str:
        SINGLE_FILE.write(f'{SINGLE},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    elif "Double" in display_str:
        DOUBLE_FILE.write(f'{DOUBLE},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    elif "Triple" in display_str:
        TRIPLE_FILE.write(f'{TRIPLE},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    elif "Home Run" in display_str:
        HR_FILE.write(f'{HOME_RUN},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')

def handle_flyout(cur_pitcher, cur_batter, named_defender):
    CONTACT_OUT_FILE.write(f'{FLYOUT},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    FLYOUT_FILE.write(f'{FLYOUT},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')

def handle_groundout(cur_pitcher, cur_batter, named_defender, display_str):
    CONTACT_OUT_FILE.write(f'{FLYOUT},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    GROUNDOUT_FILE.write(f'{FLYOUT},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')
    if "choice" in display_str or "forced out at Second" in display_str or "forced out at Third" in display_str or "forced out at Home" in display_str:
        FC_FILE.write(f'{FIELDERS_CHOICE},{feature_map[cur_batter]},{feature_map[cur_pitcher]},{feature_map[named_defender]}\n')

feature_map = {}
with open(player_file, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        id = row[1]
        feature_map[id] = ",".join(row[6:59])
        #print(f'{row[2]} == |{feature_map[id]}|')

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

            ball_or_strike = re.search("\d-\d", display_str)
            if ball_or_strike or " walk" in display_str or "Ball 4" in display_str or " strikes" in display_str:
                if " walk" in display_str or "Ball" in display_str:
                    handle_ball(cur_pitcher, cur_batter, display_str)
                if "trike" in display_str:
                    handle_strike(cur_pitcher, cur_batter, display_str)
                if "Foul" in display_str or "foul" in display_str or "out of play" in display_str:
                    handle_foul(cur_pitcher, cur_batter)

            if named_defender == '':
                print("EMPTY DEFENDER")
                continue
            if "Single" in display_str or "Double" in display_str or "Triple" in display_str or "Home Run" in display_str:
                handle_hit(cur_pitcher, cur_batter, named_defender, display_str)

            if " makes" in display_str or "to make" in display_str or "ly out" in display_str:
                handle_flyout(cur_pitcher, cur_batter, named_defender)

            if "roundout" in display_str or "forced out" in display_str:
                handle_groundout(cur_pitcher, cur_batter, named_defender, display_str)
