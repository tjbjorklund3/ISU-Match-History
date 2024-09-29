import sqlite3
import json
import os
from config import db_file_path, json_folder_path

# Load the unique keys from the json_keys.txt
def load_json_keys():
    keys = set()
    with open('json_keys.txt', 'r') as file:
        for line in file:
            keys.add(line.strip())
    return keys

# Function to ensure the table has all required columns
def ensure_columns_exist(cursor, table_name, columns):
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = set(row[1] for row in cursor.fetchall())
    
    missing_columns = columns - existing_columns
    
    for column in missing_columns:
        # Dynamically add missing columns, all stored as TEXT for simplicity
        alter_table_sql = f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT"
        cursor.execute(alter_table_sql)

# Function to insert or update a match and participants data into the database
def insert_or_update_match_data(cursor, match_data, participants_data):
    # Extract match-level data
    match_id = match_data.get('matchId')
    
    # Insert or update match data
    match_columns = ', '.join(match_data.keys())
    match_placeholders = ', '.join('?' * len(match_data))
    match_values = list(match_data.values())
    
    cursor.execute(f"""
        INSERT OR REPLACE INTO matches ({match_columns}) 
        VALUES ({match_placeholders})
    """, match_values)
    
    # Insert participants data
    for participant in participants_data:
        participant_columns = ', '.join(participant.keys())
        participant_placeholders = ', '.join('?' * len(participant))
        participant_values = list(participant.values())
        
        cursor.execute(f"""
            INSERT INTO participants (matchId, {participant_columns}) 
            VALUES (?, {participant_placeholders})
        """, [match_id] + participant_values)

# Main function to process JSON files and store data in the database
def process_json_to_db():
    # Load all unique JSON keys
    all_keys = load_json_keys()
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    
    # Iterate through all JSON files in the folder
    for file_name in os.listdir(json_folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(json_folder_path, file_name)
            try:
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    
                    # Ensure the 'matches' table contains all necessary columns
                    ensure_columns_exist(cursor, 'matches', all_keys)
                    ensure_columns_exist(cursor, 'participants', all_keys)

                    # Process match data and participant data
                    match_data = {key: json_data[key] for key in json_data if key != 'participants'}
                    participants_data = json_data.get('participants', [])

                    # Insert or update match and participant data into the database
                    insert_or_update_match_data(cursor, match_data, participants_data)

                    print(f"Processed file: {file_name}")
            
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Config File Loaded")
    process_json_to_db()

