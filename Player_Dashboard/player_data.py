# Player_Dashboard/player_data.py

from Player_Dashboard.data_loading import load_data, save_data, normalize_string
from Player_Dashboard.data_processing import calculate_kda_and_cs, convert_duration
from Player_Dashboard.column_mapping import rename_columns, column_order
from Player_Dashboard.rendering import render_player_data
from Player_Dashboard.lifetime_stats_cards import display_lifetime_stats_cards  # Import the lifetime stats card
import streamlit as st
from Player_Dashboard.aliases import aliases
import pandas as pd
from Player_Dashboard.role_images import role_images  # Import role images from role_images.py

# Helper function to create a tuple with player name and image URL
def create_dropdown_options():
    dropdown_options = []
    for player, image_path in role_images.items():
        dropdown_options.append((player, image_path))
    return dropdown_options

def display_player_data():
    # **Refresh Data button placed above the table**
    if st.button("Refresh Data"):
        st.cache_data.clear()  # Clear the cache to force reloading the updated CSV
        st.set_query_params()  # Update the query params without experimental warning

    # **Load the data**
    df = load_data()

    # **Rename columns for better readability**
    df = rename_columns(df)

    # **Ensure WIN column has 'Lose' instead of 'Fail'**
    if 'WIN' in df.columns:
        df['WIN'] = df['WIN'].replace('Fail', 'Lose')  # Replace 'Fail' with 'Lose'

    # **Check if the 'Player' column exists after renaming**
    if 'Player' not in df.columns:
        st.error("The 'Player' column is missing from the dataset.")
        return

    # **Normalize player names in the dataframe**
    df['Player'] = df['Player'].apply(normalize_string)

    # Create dropdown options with player name and their image URL
    player_options_with_images = create_dropdown_options()

    # Selectbox to display player names along with icons
    selected_option = st.selectbox('Select a Player', player_options_with_images, format_func=lambda x: f"{x[0]}")

    # Extract the actual player name
    player_name, _ = selected_option

    # Display the player's role image above the dropdown
    ###st.image(selected_option[1], width=50)

    # **Get the aliases for the selected player and normalize them**
    player_aliases = [normalize_string(alias) for alias in aliases[player_name]]

    # **Filter data based on selected player aliases**
    player_df = df[df['Player'].isin(player_aliases)]

    # **Check if player data exists**
    if player_df.empty:
        st.write(f"No data found for player {player_name}")
        return

    # **Calculate KDA and CS per minute**
    player_df = calculate_kda_and_cs(player_df)

    # **Convert game duration to readable format**
    if 'Game Length' in player_df.columns:
        player_df['Game Length'] = player_df['Game Length'].apply(convert_duration)

    # **Reorder columns as per the new column_order**
    player_df = player_df[column_order]

    # **Render the player data using AgGrid (This is the main table)**
    grid_response = render_player_data(player_df)

    # **Detect if data was edited by comparing the returned data**
    updated_df = pd.DataFrame(grid_response['data'])  # Get the updated data from the grid
    data_edited = not player_df.equals(updated_df)  # Compare the original dataframe to the updated one

    # **Save button appears below the table if edits have been made**
    if data_edited:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some space before the button
        with st.container():
            st.write("**You have unsaved changes!**")  # Show a subtle message
            if st.button("Save Changes", help="Click to save any edits you made to the data"):
                save_data(updated_df)
                st.success(f"Data for {player_name} saved successfully!")

    # **Lifetime stats dropdown**
    with st.expander("Show Lifetime Stats"):
        # Add a champion filter for lifetime stats (default is all champions)
        unique_champions = player_df['Champion'].unique().tolist()
        unique_champions.insert(0, "All Champions")  # Add 'All Champions' option to the list
        selected_champion = st.selectbox("Filter by Champion", unique_champions)

        # Filter data by selected champion (if not "All Champions")
        if selected_champion != "All Champions":
            filtered_df = player_df[player_df['Champion'] == selected_champion]
        else:
            filtered_df = player_df

        # **Winrate Calculation**
        total_games = len(filtered_df)
        total_wins = filtered_df['WIN'].value_counts().get('Win', 0)  # Count the 'Win' entries
        winrate = (total_wins / total_games * 100) if total_games > 0 else 0
        st.write(f"Winrate: {winrate:.2f}% ({total_wins}/{total_games} Wins)")

        # Display lifetime stats card for the selected player (filtered by champion if selected)
        display_lifetime_stats_cards(filtered_df)  # Pass the filtered player data to the lifetime stats card
