#!bin/python3

import json

cur_file = "../data/s1/raw/players.json"
stlats = [
    'Sight',
    'Thwack',
    'Ferocity',
    'Control',
    'Stuff',
    'Guile',
    'Reach',
    'Magnet',
    'Reflex',
    'Hustle',
    'Stealth',
    'Dodge',
    'Thrive',
    'Survive',
    'Drama'
]
hmLen = 36

with open(cur_file) as json_file:
    raw_data = json.load(json_file)
    stat_header = ''
    for stat in stlats:
        stat_header += f',{stat}'
    hm_header = ''
    for x in range(0, 36):
        hm_header += f',hm_{x}'
    print(f'team_id,id,name,team,roster_location,roster_order,pos_x,pos_y{stat_header}{hm_header}')
    first = True
    with open("../data/s1/players/processed_players.csv", "w") as OUT_FILE:
        for player in raw_data:
            attributes = player['attributes']
            id = player['id']
            name = player['name']
            roster_loc = player['rosterSlots'][0]['location']
            roster_pos = player['rosterSlots'][0]['orderIndex']
            heatMap = player['playerHeatMaps']
            pos_x = player['positions'][0]['x']
            pos_y = player['positions'][0]['y']
            team_id = player['team']['id']
            team_name = player['team']['name']
            stat_str = ''
            hm_str = ''
            stat_count = 0
            for stat in attributes:
                if stat['name'] != stlats[stat_count]:
                    exit(-1)
                stat_count += 1
                stat_str += f',{stat["value"]}'
            for hm in heatMap:
                hm_str += f',{hm["currentValue"]}'

            print(f'{team_id},{id},{name},{team_name},{roster_loc},{roster_pos},{pos_x},{pos_y}{stat_str}{hm_str}')
            if first:
                OUT_FILE.write(f'team_id,id,name,team,roster_location,roster_order,pos_x,pos_y{stat_header}{hm_header}')
                OUT_FILE.write("\n")
            first = False
            OUT_FILE.write(f'{team_id},{id},{name},{team_name},{roster_loc},{roster_pos},{pos_x},{pos_y}{stat_str}{hm_str}')
            OUT_FILE.write("\n")
        OUT_FILE.close()
        #exit(0)
