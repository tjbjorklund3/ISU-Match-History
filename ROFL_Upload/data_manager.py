import json

# Load opponents from the JSON file
def load_opponents(filepath='ROFL_Upload/opponents.json'):
    with open(filepath, 'r') as f:
        opponents_data = json.load(f)
    return opponents_data['Amateur Teams']

# Load events from the events.json file
def load_events(filepath='ROFL_Upload/events.json'):
    with open(filepath, 'r') as f:
        events_data = json.load(f)
    return events_data['events']

# Add a new team to the opponents.json file
def add_new_team(team_name, filepath='ROFL_Upload/opponents.json'):
    with open(filepath, 'r+') as f:
        opponents_data = json.load(f)
        opponents_data['Amateur Teams'].append(team_name)

        f.seek(0)
        json.dump(opponents_data, f, indent=4)
        f.truncate()
