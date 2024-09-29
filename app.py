import streamlit as st
import calculate_stats
import player_data  # A new file for player data page

# Main function to handle navigation between pages
def main():
    st.title("League of Legends Dashboard")

    # Use a sidebar to select the page
    page = st.sidebar.selectbox("Select a page", ["PCL Champion Kills", "Player Data"])

    # Navigate based on the selected page
    if page == "PCL Champion Kills":
        calculate_stats.display_pcl_champions_and_kills()  # The original PCL stats page
    elif page == "Player Data":
        player_data.display_player_data()  # New Player Data page


if __name__ == "__main__":
    main()
