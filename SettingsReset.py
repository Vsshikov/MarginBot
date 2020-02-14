import json


settings = {
    'total_round_num': 0,
    'rounds': [],
    'total_team_num': 0,
    'total_actives_num': 0,
    'teams': [],
}

with open('Settings.json', 'w+') as event_file:
    json.dump(settings, event_file, indent=4)