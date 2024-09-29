import streamlit as st
import player_data

def main():
    st.title("🚀 PCL Player Stats Dashboard - TESTING CHANGES 🚀")

    st.write("### This is a big test to ensure changes are being reflected on the live deployment. If you see this message, it means the changes are working!")

    # Call the function to display the player data
    player_data.display_player_data()  # Player Data page

if __name__ == "__main__":
    main()
