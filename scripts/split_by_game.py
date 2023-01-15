#!bin/python3

import json

game_events = {}

for x in range(0, 207):
    cur_file = f'../data/s1/raw/game_{x}.json'
    with open(cur_file) as json_file:
        raw_data = json.load(json_file)
        for event in raw_data:
            game_id = event['game_id']
            if game_id not in game_events:
                game_events[game_id] = []
            game_events[game_id].append(event)

for game_id in game_events:
    cur_events = game_events[game_id]
    cur_events.sort(key=lambda x: x['data']['displayOrder'])

    json_events = json.dumps(cur_events, indent=4)
    out_file = f'../data/s1/games/{game_id}.json'
    with open(out_file, "w") as outfile:
        outfile.write(json_events)



