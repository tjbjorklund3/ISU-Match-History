import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from aliases import aliases  # Import aliases for players
from player_data_labels import column_labels, column_order  # Import labels and column order

# Load data from CSV
@st.cache_data
def load_data():
    df = pd.read_csv('aggregated_replays_data.csv')
    return df

# Save updated data back to CSV
def save_data(df):
    df.to_csv('aggregated_replays_data.csv', index=False)
    st.success("Changes saved successfully!")

# Normalize strings: lower case and strip whitespace
def normalize_string(s):
    return str(s).strip().lower()

# Rename columns for better readability
def rename_columns(df):
    return df.rename(columns=column_labels)

# Display editable table for player data
def display_player_data():
    # Load the data
    df = load_data()

    # Debug: Show the actual player names in the CSV after normalization
    print("Before normalization, player names in the CSV:")
    print(df[['NAME']].drop_duplicates())  # Output unique names in the CSV

    # Normalize player names in the dataframe
    df['NAME'] = df['NAME'].apply(normalize_string)

    # Debug: After normalization, print unique player names in the CSV
    print("After normalization, player names in the CSV:")
    print(df[['NAME']].drop_duplicates())

    # Add player selection dropdown based on aliases
    player_name = st.selectbox('Select a Player', list(aliases.keys()))

    # Get the aliases for the selected player and normalize them
    player_aliases = [normalize_string(alias) for alias in aliases[player_name]]

    # Debug: Print selected player and their aliases
    print(f"Selected player: {player_name}")
    print(f"Player aliases: {player_aliases}")

    # Filter data based on selected player aliases
    player_df = df[df['NAME'].isin(player_aliases)]

    # Debug: Check if any of the aliases are in the DataFrame
    print("Checking if aliases exist in the CSV...")
    for alias in player_aliases:
        if alias in df['NAME'].values:
            print(f"Alias '{alias}' found in the data!")
        else:
            print(f"Alias '{alias}' NOT found in the data.")

    # Check if player data exists
    if player_df.empty:
        st.write(f"No data found for player {player_name}")
        print(f"No data found for player {player_name}")
        return

    # Rename columns for better readability
    player_df = rename_columns(player_df)

    # Rearrange columns according to predefined order
    player_df = player_df[column_order]

    # Configure grid options for AgGrid
    gb = GridOptionsBuilder.from_dataframe(player_df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Pagination for large datasets
    gb.configure_side_bar()  # Enable sidebar filters
    gb.configure_default_column(editable=True, filter=True, resizable=True)  # Columns are editable and filterable
    gb.configure_grid_options(domLayout='autoHeight')  # Automatically adjusts height of the grid

    # Set custom column widths if needed (Optional)
    gb.configure_columns(
        ['Kills', 'Deaths', 'Assists'], 
        width=80  # Example: Adjust width of these columns
    )

    gridOptions = gb.build()

    # Display the editable table using AgGrid
    grid_response = AgGrid(
        player_df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=True,
        theme="streamlit",  # Theme: balham, material, etc.
        enable_enterprise_modules=True,
        height=2000,  # Adjust height for better user experience
        width='200%',
    )

    # Get the updated data from the grid
    updated_df = pd.DataFrame(grid_response['data'])

    # Display a save button to store the edited data back to the CSV
    if st.button("Save Changes"):
        save_data(updated_df)

    # Debug: Display a confirmation message in PowerShell after saving
    print(f"Data for {player_name} saved successfully!")

