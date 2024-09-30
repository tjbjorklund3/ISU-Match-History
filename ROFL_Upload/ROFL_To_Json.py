#ROFL_To_Json.py

import json
import os
import re
import shutil
import requests
import config

version_pattern = r'(\d{1,2}\.\d{1,2}\.\d{3,4}\.\d{3,4})'

# Fetch the latest game versions from Riot API (moved to utils.py)
def fetch_latest_versions():
    url = config.RIOT_API_VERSIONS_URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error fetching versions from Riot API: {e}')
        return []

def extract_game_version_from_file(data_str):
    version_matches = re.findall(version_pattern, data_str)
    if version_matches:
        print(f"Version-like strings found: {version_matches}")
        return version_matches[0]
    else:
        print("No version-like string found in the file.")
        return None

def process_rofl_file(input_file_path, output_file_path, match_id, latest_versions):
    try:
        print(f'Processing {input_file_path}...')

        # Open the .rofl file in binary read mode
        with open(input_file_path, 'rb') as file:
            # Decode the binary data to a string, ignoring undecodable bytes
            data_str = file.read().decode('utf-8', 'ignore')

        # Extract the game version using the new logic
        game_version_value = extract_game_version_from_file(data_str)

        if game_version_value:
            print(f"Extracted game version: '{game_version_value}'")
        else:
            print(f"Failed to extract a valid game version from {input_file_path}")
            game_version_value = 'Unknown'

        # Check if extracted version matches any from Riot's official version list
        if game_version_value != 'Unknown':
            for version in latest_versions:
                if game_version_value.startswith(version[:5]):
                    print(f"Matched extracted version '{game_version_value}' with Riot version '{version}'")
                    game_version_value = version
                    break
            else:
                print(f"No match found for game version '{game_version_value}' in Riot versions")
                game_version_value = 'Unknown'

        # Extract gameLength and statsJson
        json_start_str = '{"gameLength":'
        json_end_str = '}]"}'

        # Find the start and end indices of JSON data
        start_idx = data_str.find(json_start_str)
        if start_idx == -1:
            print(f'JSON start string {json_start_str} not found in {input_file_path}')
            return

        end_idx = data_str.find(json_end_str, start_idx)
        if end_idx == -1:
            print(f'JSON end string {json_end_str} not found in {input_file_path}')
            return

        # Extract and clean JSON data
        end_idx += len(json_end_str)
        json_str = data_str[start_idx:end_idx]
        corrected_data_str = json_str.replace('\\"', '"')

        # Extract gameLength and statsJson
        game_length_start_idx = corrected_data_str.find('"gameLength":') + len('"gameLength":')
        game_length_end_idx = corrected_data_str.find(',', game_length_start_idx)
        game_length_value = corrected_data_str[game_length_start_idx:game_length_end_idx].strip()

        stats_json_start_idx = corrected_data_str.find('"statsJson":"[') + len('"statsJson":"')
        stats_json_end_idx = corrected_data_str.rfind('"}')
        stats_json_str = corrected_data_str[stats_json_start_idx:stats_json_end_idx].replace('\\"', '"')

        # Convert the statsJson string to Python dictionary
        stats_json = json.loads(stats_json_str)

        # Create the final formatted dictionary
        formatted_dict = {
            "matchId": match_id,
            "gameDuration": game_length_value,
            "gameVersion": game_version_value,
            "participants": stats_json
        }

        # Write the formatted dictionary to the output file in JSON format
        with open(output_file_path, 'w') as out_file:
            json.dump(formatted_dict, out_file, indent=2)

        print(f'Successfully processed {input_file_path} and wrote to {output_file_path}')

        # Move the processed file to the "Processed" folder
        processed_file_path = os.path.join(config.PROCESSED_DIRECTORY, os.path.basename(input_file_path))
        shutil.move(input_file_path, processed_file_path)
        print(f'Moved {input_file_path} to {processed_file_path}')

    except Exception as e:
        print(f'Error processing {input_file_path}: {str(e)}')
