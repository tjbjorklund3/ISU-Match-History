import pandas as pd
import os
import config  # Import the config.py file for directory paths

# Function to update the DataFrame with new data
def main():
    print("Checking for new JSON data to add to DataFrame...")

    # Path for the aggregated DataFrame CSV
    aggregated_csv_path = 'aggregated_replays_data.csv'

    # Load the existing DataFrame if it exists, or create a new one if not
    if os.path.exists(aggregated_csv_path):
        final_df = pd.read_csv(aggregated_csv_path)
        existing_match_ids = set(final_df['matchID'].astype(str))  # Ensure matchID is treated as string for comparison
        print(f"Found {len(existing_match_ids)} existing matches in the DataFrame.")
    else:
        final_df = pd.DataFrame()  # Create an empty DataFrame
        existing_match_ids = set()  # No match IDs exist yet
        print("No existing DataFrame found, creating a new one.")

    # Process new JSON files from the JSON directory
    json_files = [file for file in os.listdir(config.JSON_DIRECTORY) if file.endswith('.json')]

    if not json_files:
        print("No JSON files found in the JSON directory.")
        return

    # Initialize an empty list for new data
    new_data = []

    for file in json_files:
        # Load each JSON file
        file_path = os.path.join(config.JSON_DIRECTORY, file)
        df = pd.read_json(file_path)

        # Extract matchID and treat it as a string
        matchID = str(df['matchId'][0])

        # Remove any potential prefix (e.g., "NA1-")
        matchID_clean = matchID.split('-')[-1]

        # Skip if the matchID is already in the DataFrame
        if matchID_clean in existing_match_ids:
            print(f"Match {matchID_clean} already exists in the DataFrame, skipping...")
            continue

        # Process participant-level data
        participants = []
        for i in range(len(df['participants'])):
            participants.append(pd.Series(df['participants'][i]))

        # Create a DataFrame from participants
        participants_df = pd.DataFrame(participants)

        # Add matchID, gameDuration, and gameVersion columns to participants DataFrame
        match_df = pd.DataFrame({
            'matchID': matchID_clean,
            'gameDuration': df['gameDuration'],
            'gameVersion': df['gameVersion']
        }).join(participants_df)

        # Debug: Show the structure of the new match data
        print(f"Processed match {matchID_clean} with {len(participants)} participants.")

        # Append this match data to the new data list
        new_data.append(match_df)

    # Check if there is new data to add
    if new_data:
        # Concatenate new data and add it to the existing DataFrame
        new_df = pd.concat(new_data, ignore_index=True)
        final_df = pd.concat([final_df, new_df], ignore_index=True)

        # Save the updated DataFrame
        final_df.to_csv(aggregated_csv_path, index=False)
        print(f"Updated DataFrame saved with {len(final_df)} total matches.")
    else:
        print("No new data to add to the DataFrame.")

if __name__ == "__main__":
    main()
