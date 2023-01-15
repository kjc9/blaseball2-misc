#!bin/python3

import json

game_list = "../data/s1/games-list.txt"
string_file = "../data/s1/processed/generic_strings.txt"
out_file = open(string_file, "w")
with open(game_list, "r") as read_file:
    lines = read_file.readlines()
files = []
for line in lines:
    line = line.replace("\n", "")
    files.append(line)

#files = ["01c74980-5747-4450-b30c-b86d341705a5.json"]

for file in files:
    cur_batter = ""
    cur_pitcher = ""
    cur_def_arr = []
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
                    cur_batter = event['data']['changedState']['batter']['name']
                    if cur_batter.startswith('DeAndre') and cur_batter.endswith('Possum'):
                        cur_batter = "DeAndre OPossum"
                    if cur_batter.startswith('Carter') and cur_batter.endswith('connor'):
                        cur_batter = "Carter Oconnor"

                if event['data']['changedState']['pitcher'] != None:
                    cur_pitcher = event['data']['changedState']['pitcher']['name']
                cur_def_arr = []
                for defender in event['data']['changedState']['defenders']:
                    if defender['name'].startswith('DeAndre') and defender['name'].endswith('Possum'):
                        defender['name'] = "DeAndre OPossum"
                    if defender['name'].startswith('Carter') and defender['name'].endswith('connor'):
                        defender['name'] = "Carter Oconnor"
                    cur_def_arr.append(defender['name'])
            if 'baserunners' in event['data']['changedState']:
                #cur_runner_arr = []
                for runner in event['data']['changedState']['baserunners']:
                    if runner['name'].startswith('DeAndre') and runner['name'].endswith('Possum'):
                        runner['name'] = "DeAndre OPossum"
                    if runner['name'].startswith('Carter') and runner['name'].endswith('connor'):
                        runner['name'] = "Carter Oconnor"
                    cur_runner_arr.append(runner['name'])
            display_str = event['data']['displayText']
            display_str = display_str.replace('Carter O&#x27;connor', 'Carter Oconnor').replace('DeAndre O&#x27;Possum', 'DeAndre OPossum')
            if display_str == 'Play Ball!' or display_str.startswith("End of the"):
                continue

            generic_str = display_str.replace(cur_batter, "BATTER").replace(cur_pitcher, "PITCHER")
            generic_str = generic_str\
                .replace("0-1", "X-X")\
                .replace("0-2", "X-X")\
                .replace("1-0", "X-X")\
                .replace("1-1", "X-X")\
                .replace("1-2", "X-X")\
                .replace("1-3", "X-X")\
                .replace("2-0", "X-X")\
                .replace("2-1", "X-X")\
                .replace("2-2", "X-X")\
                .replace("3-0", "X-X")\
                .replace("3-1", "X-X")\
                .replace("3-2", "X-X")
            for name in cur_def_arr:
                generic_str = generic_str.replace(name, "DEFENDER")
            for name in cur_runner_arr:
                generic_str = generic_str.replace(name, "RUNNER")
            if generic_str != "":
                out_file.write(f'{generic_str}\n')
                #print(f'|{generic_str}|')
            generic_str = ""
    #exit(0)