import json

def extract_data_from_json(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
    
    match_id = json_data.get('matchId', 'Unknown')
    game_duration = json_data.get('gameDuration', 'Unknown')
    game_version = json_data.get('gameVersion', 'Unknown')
    
    participants = []
    for participant in json_data.get('participants', []):
        participants.append({
            'assists': participant.get('ASSISTS', 0),
            'kills': participant.get('KILLS', 0),
            'deaths': participant.get('DEATHS', 0),
            'champion': participant.get('SKIN', 'Unknown'),
            'team_position': participant.get('TEAM_POSITION', 'Unknown')
        })

    return {
        'matchId': match_id,
        'gameDuration': game_duration,
        'gameVersion': game_version,
        'participants': participants
    }
