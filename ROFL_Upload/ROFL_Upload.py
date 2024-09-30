import streamlit as st
from ROFL_Upload.file_manager import save_uploaded_file
from ROFL_Upload.data_manager import load_opponents, load_events, add_new_team
from ROFL_Upload.rofl_processing import process_rofl_files
from ROFL_Upload.utils import fetch_latest_versions
from ROFL_Upload.Add_to_MatchHistory import update_match_history_dataframe

def upload_rofl_file():
    st.header("Upload ROFL Files")

    # Load the list of opponents and events
    opponents = load_opponents()
    events = load_events()

    # Allow multiple ROFL files to be uploaded
    uploaded_files = st.file_uploader("Choose ROFL files", type=["rofl"], accept_multiple_files=True)

    if uploaded_files:
        # Opponent selection
        opponents_with_other = opponents + ["Other (Add new team)"]
        selected_opponent = st.selectbox("Select Opponent", opponents_with_other)

        if selected_opponent == "Other (Add new team)":
            new_team = st.text_input("Enter the new team's name:")
            if new_team and st.button("Add New Team"):
                add_new_team(new_team)
                selected_opponent = new_team

        # Event and playoffs selection
        selected_event = st.selectbox("Select Event", events)
        is_playoffs = st.checkbox("Is this match a playoff game?")

        # Save the uploaded files and process each one
        for uploaded_file in uploaded_files:
            uploaded_file_path = save_uploaded_file(uploaded_file)
            st.success(f"File {uploaded_file.name} uploaded successfully with opponent: {selected_opponent}")

            # Fetch the latest Riot versions
            latest_versions = fetch_latest_versions()

            # Process the ROFL files
            process_rofl_files(uploaded_file_path, selected_event, is_playoffs, latest_versions)

        # Button to trigger adding data to the DataFrame
        if st.button("Add Processed Files to Match History"):
            update_match_history_dataframe()
            st.success("New JSON files added to match history DataFrame.")
