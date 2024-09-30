# app.py

import streamlit as st
from Player_Dashboard import player_data
import calculate_stats
from ROFL_Upload.ROFL_Upload import upload_rofl_file

# Main function to handle navigation between pages
def main():
    st.title("League of Legends Dashboard")

    # Use a sidebar to select the page
    page = st.sidebar.selectbox("Select a page", ["Player Data", "Upload ROFL Files"])

    # Navigate based on the selected page
    if page == "Player Data":
        player_data.display_player_data()  # Player Data page
    elif page == "Upload ROFL Files":
        upload_rofl_file()  # Upload ROFL files page

if __name__ == "__main__":
    main()
