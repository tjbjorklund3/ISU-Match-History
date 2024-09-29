import sqlite3
import os

# Load the path from config.py or define it directly
from config import db_file_path

# Function to create a table if it doesn't exist
def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            matchId TEXT PRIMARY KEY,
            gameDuration TEXT,
            gameVersion TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            participantId INTEGER PRIMARY KEY AUTOINCREMENT,
            matchId TEXT,
            team TEXT,
            position TEXT,
            name TEXT,
            champion TEXT,
            FOREIGN KEY (matchId) REFERENCES matches (matchId)
        )
    ''')
    conn.commit()

# Function to update or insert the match data
def update_database(match_data):
    conn = sqlite3.connect(db_file_path)  # Connect to SQLite database
    create_table_if_not_exists(conn)
    cursor = conn.cursor()

    # Check if the matchId already exists in the database
    cursor.execute('SELECT * FROM matches WHERE matchId = ?', (match_data['matchId'],))
    result = cursor.fetchone()

    if result:
        # If the match already exists, update it (if needed)
        cursor.execute('''
            UPDATE matches SET gameDuration = ?, gameVersion = ?
            WHERE matchId = ?
        ''', (match_data['gameDuration'], match_data['gameVersion'], match_data['matchId']))
    else:
        # If the match does not exist, insert it
        cursor.execute('''
            INSERT INTO matches (matchId, gameDuration, gameVersion)
            VALUES (?, ?, ?)
        ''', (match_data['matchId'], match_data['gameDuration'], match_data['gameVersion']))

    # Update or insert participant data
    for participant in match_data['participants']:
        cursor.execute('''
            INSERT INTO participants (matchId, team, position, name, champion)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            match_data['matchId'],
            participant['team'],
            participant['position'],
            participant['name'],
            participant['champion']
        ))

    conn.commit()  # Commit the changes
    conn.close()   # Close the database connection
