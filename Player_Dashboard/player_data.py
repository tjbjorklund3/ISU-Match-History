# Player_Dashboard/player_data.py

# Main orchestrator file that calls everything together
from Player_Dashboard.data_loading import load_data, save_data, normalize_string
from Player_Dashboard.data_processing import calculate_kda_and_cs, convert_duration
from Player_Dashboard.column_mapping import rename_columns, column_order
from Player_Dashboard.rendering import render_player_data
import streamlit as st
from Player_Dashboard.aliases import aliases

def display_player_data():
    # Button to clear cache manually (for debugging or after adding new data)
    if st.button("Refresh Data"):
        st.cache_data.clear()  # Clear the cache to force reloading the updated CSV

    # Load the data
    df = load_data()

    # Normalize player names in the dataframe
    df['NAME'] = df['NAME'].apply(normalize_string)

    # Add player selection dropdown based on aliases
    player_name = st.selectbox('Select a Player', list(aliases.keys()))

    # Get the aliases for the selected player and normalize them
    player_aliases = [normalize_string(alias) for alias in aliases[player_name]]

    # Filter data based on selected player aliases
    player_df = df[df['NAME'].isin(player_aliases)]

    # Check if player data exists
    if player_df.empty:
        st.write(f"No data found for player {player_name}")
        return

    # Rename columns for better readability
    player_df = rename_columns(player_df)

    # Calculate KDA and CS per minute
    player_df = calculate_kda_and_cs(player_df)

    # Convert game duration to readable format
    if 'Game Length' in player_df.columns:
        player_df['Game Length'] = player_df['Game Length'].apply(convert_duration)

    # Reorder columns as per the new column_order
    player_df = player_df[column_order]

    # Render the player data using AgGrid
    grid_response = render_player_data(player_df)

    # Get the updated data from the grid
    updated_df = grid_response['data']

    # Display a save button to store the edited data back to the CSV
    if st.button("Save Changes"):
        save_data(updated_df)

    # Debug: Display a confirmation message in PowerShell after saving
    print(f"Data for {player_name} saved successfully!")
