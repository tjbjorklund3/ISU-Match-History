import pandas as pd
import streamlit as st

# Load data from CSV
@st.cache_data
def load_data():
    df = pd.read_csv('aggregated_replays_data.csv')
    return df

# Filter data for PCL
def filter_data_for_pcl(df):
    return df[df['NAME'] == "PCL"]  # Filter DataFrame where NAME is PCL

# Function to display PCL's champions and kills
def display_pcl_champions_and_kills():
    # Load the data
    df = load_data()

    # Filter the data for PCL
    pcl_df = filter_data_for_pcl(df)

    # Check if PCL has any data
    if pcl_df.empty:
        st.write("No data found for PCL")
        return

    # Get unique champions (characters) PCL has played
    unique_champions = pcl_df['SKIN'].unique()

    # Allow the user to select a champion
    selected_champion = st.selectbox("Select a Champion", unique_champions)

    # Further filter the data based on the selected champion
    if selected_champion:
        champion_df = pcl_df[pcl_df['SKIN'] == selected_champion]

        if not champion_df.empty:
            # Show the CHAMPIONS_KILLED for the selected champion
            st.subheader(f"Champion Kills for PCL playing {selected_champion}")
            total_kills = champion_df['CHAMPIONS_KILLED'].sum()
            st.write(f"Total Kills: {total_kills}")

            # Show detailed breakdown of games and kills
            st.dataframe(champion_df[['matchID', 'gameDuration', 'CHAMPIONS_KILLED']])
        else:
            st.write(f"No data available for PCL playing {selected_champion}")
