# ROFL_Upload.py
import streamlit as st
import os
import shutil
import json
import time
from config import ROFL_DIRECTORY, JSON_DIRECTORY, PROCESSED_DIRECTORY
from ROFL_To_JSON import process_rofl_file
from ROFL_Upload.Add_to_MatchHistory import update_match_history_dataframe
from ROFL_Upload.utils import fetch_latest_versions  # Ensure correct import of utils

# Load opponents from the JSON file
def load_opponents():
    with open('ROFL_Upload/opponents.json', 'r') as f:
        opponents_data = json.load(f)

    opponents = []
    for teams in opponents_data.values():
        opponents.extend(teams)

    return opponents

# Define the function for uploading .rofl files
def upload_rofl_file():
    st.header("Upload ROFL Files")

    # Load the list of opponents from the JSON file
    opponents = load_opponents()

    # File uploader widget for .rofl files
    uploaded_file = st.file_uploader("Choose a ROFL file", type=["rofl"])

    # Ensure that a file is uploaded
    if uploaded_file is not None:
        # Display file details
        st.write("Filename:", uploaded_file.name)

        # Allow user to select or add a new opponent
        opponents_with_other = opponents + ["Other (Add new team)"]
        selected_opponent = st.selectbox("Select Opponent", opponents_with_other)

        # If "Other" is selected, show a text input for adding a new team
        if selected_opponent == "Other (Add new team)":
            new_team = st.text_input("Enter the new team's name:")
            if new_team:
                selected_opponent = new_team
                if st.button("Add New Team"):
                    add_new_team(new_team)

        # Ensure that the ROFL directory exists
        if not os.path.exists(ROFL_DIRECTORY):
            os.makedirs(ROFL_DIRECTORY)

        # Save the uploaded file to the ROFL directory
        uploaded_file_path = os.path.join(ROFL_DIRECTORY, uploaded_file.name)
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File {uploaded_file.name} uploaded successfully with opponent: {selected_opponent}")

        # Fetch the latest Riot versions for processing
        latest_versions = fetch_latest_versions()

        # Process the uploaded ROFL file after uploading
        process_rofl_files(latest_versions)

        # Button to trigger adding data to the DataFrame
        if st.button("Add Processed Files to Match History"):
            update_match_history_dataframe()
            st.success("New JSON files added to match history DataFrame.")

# Add a new team to the opponents.json file
def add_new_team(team_name):
    with open('ROFL_Upload/opponents.json', 'r+') as f:
        opponents_data = json.load(f)
        opponents_data['Amateur Teams'].append(team_name)

        f.seek(0)
        json.dump(opponents_data, f, indent=4)
        f.truncate()

    st.success(f"New team '{team_name}' added successfully!")

# Retry logic for moving files in case of errors
def safe_move_file(src, dest, retries=3, delay=1):
    for attempt in range(retries):
        try:
            # Check if the file has already been moved
            if os.path.exists(dest):
                return True

            shutil.move(src, dest)
            return True
        except Exception as e:
            time.sleep(delay)

    # Final check: If file has been moved after retries, log success
    if os.path.exists(dest):
        return True

    return False

# Process any ROFL files in the ROFL_DIRECTORY
def process_rofl_files(latest_versions):
    rofl_files = [f for f in os.listdir(ROFL_DIRECTORY) if f.endswith('.rofl')]

    for rofl_file in rofl_files:
        rofl_file_path = os.path.join(ROFL_DIRECTORY, rofl_file)
        match_id = rofl_file.split('.')[0]

        json_output_path = os.path.join(JSON_DIRECTORY, f"{match_id}.json")

        if not os.path.exists(JSON_DIRECTORY):
            os.makedirs(JSON_DIRECTORY)

        # Process the ROFL file and generate the JSON
        process_rofl_file(rofl_file_path, json_output_path, match_id, latest_versions)

        # Add a small delay before moving the processed file
        time.sleep(1)  # Wait 1 second to ensure file is fully ready to be moved

        # Move the processed ROFL file to the PROCESSED_DIRECTORY using safe move logic
        processed_file_path = os.path.join(PROCESSED_DIRECTORY, rofl_file)
        if not os.path.exists(PROCESSED_DIRECTORY):
            os.makedirs(PROCESSED_DIRECTORY)

        if safe_move_file(rofl_file_path, processed_file_path):
            continue
        else:
            st.write(f"Failed to move {rofl_file} after multiple attempts.")
