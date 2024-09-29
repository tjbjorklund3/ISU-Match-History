import os
import json

# Define the directory where JSON files are stored
folder_path = r'C:\Users\TJ\Documents\League of Legends\Replays\replayscript\jsonprocesstest'

# Function to translate and extract the relevant information from each participant
def translate_participant_info(json_data):
    team_translation = {'100': 'BLUE', '200': 'RED'}
    participants = json_data.get('participants', [])
    for participant in participants:
        # Translate team number to side name
        team = team_translation.get(participant.get('TEAM', 'Unknown'), 'Unknown')
        position = participant.get('TEAM_POSITION', 'Unknown')
        name = participant.get('NAME', 'Unknown')
        champion = participant.get('SKIN', 'Unknown')
        
        # Print the translated information
        print(f"Side: {team}, Position: {position}, Name: {name}, Champion: {champion}")

# Iterate through all JSON files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Open and read the JSON file
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)
                
                # Translate and print participant info
                print(f"Processing file: {file_name}")
                translate_participant_info(json_data)
                print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")
