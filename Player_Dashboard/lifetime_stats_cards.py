# Player_Dashboard/lifetime_stats_cards.py

import streamlit as st

def display_lifetime_stats_cards(player_df):
    """
    Displays lifetime stats for a player as cards.
    """
    # Calculate global stats from player data
    total_kills = player_df['Kills'].sum()
    total_deaths = player_df['Deaths'].sum()
    total_assists = player_df['Assists'].sum()
    total_games = len(player_df)
    
    # Calculate average stats
    avg_kills = round(total_kills / total_games, 2)
    avg_deaths = round(total_deaths / total_games, 2)
    avg_assists = round(total_assists / total_games, 2)
    
    # Display card-style stats
    st.subheader("Lifetime Stats")

    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Kills", total_kills)
    col2.metric("Total Deaths", total_deaths)
    col3.metric("Total Assists", total_assists)
    
    st.write("**Average Stats Per Game**")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Avg Kills", avg_kills)
    col5.metric("Avg Deaths", avg_deaths)
    col6.metric("Avg Assists", avg_assists)
