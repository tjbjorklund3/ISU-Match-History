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

# Convert Game Length (which is in milliseconds) to minutes:seconds format without leading zeros (for display)
def convert_duration(ms):
    if pd.isna(ms):
        return "00:00"
    ms = float(ms)  # Ensure ms is numeric
    seconds = ms // 1000
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes)}:{int(seconds):02d}"

# Convert Game Length from milliseconds to total minutes (for calculations)
def get_total_minutes(ms):
    try:
        ms = float(ms)  # Ensure the value is numeric
        return ms / 1000 / 60 if pd.notna(ms) else 0
    except ValueError:
        return 0  # If ms is not a valid number, return 0

# Calculate KDA and CS per minute with rounding and handling zero values
def calculate_kda_and_cs(df):
    kills_col = 'Kills'  # Confirmed key from your provided list
    deaths_col = 'Deaths'  # Confirmed key
    assists_col = 'Assists'  # Confirmed key
    cs_col = 'Missions_CreepScore'  # Confirmed key
    game_duration_numeric_col = 'Game Length Numeric'  # Internal numeric column for game length in minutes

    # Calculate KDA: (Kills + Assists) / Deaths (if Deaths > 0)
    df['KDA'] = df.apply(lambda row: round((row[kills_col] + row[assists_col]) / row[deaths_col], 2) if row[deaths_col] > 0 else round((row[kills_col] + row[assists_col]), 2), axis=1)

    # Calculate CS per minute: Missions_CreepScore / game length (in minutes)
    def calculate_cs_per_minute(row):
        cs = row[cs_col]
        game_length_minutes = get_total_minutes(row[game_duration_numeric_col])

        # Debug: Print the values being used in the calculation
        print(f"CS: {cs}, Game Length (minutes): {game_length_minutes}, Raw gameDuration value: {row[game_duration_numeric_col]}")

        if game_length_minutes > 0:
            cs_per_minute = round(cs / game_length_minutes, 1)
        else:
            cs_per_minute = 0

        # Debug: Print the result of the calculation
        print(f"CS per Minute: {cs_per_minute}")
        return cs_per_minute

    df['CS_per_Minute'] = df.apply(calculate_cs_per_minute, axis=1)

    return df


# Rename columns for better readability
def rename_columns(df):
    return df.rename(columns=column_labels)

# Display editable table for player data
def display_player_data():
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

    # Convert 'Game Length' from ms to both a readable format and numeric format for calculations
    if 'Game Length' in player_df.columns:
        # Convert 'Game Length' to numeric values (for calculations)
        player_df['Game Length Numeric'] = pd.to_numeric(player_df['Game Length'], errors='coerce')

        # Debug: Print converted values
        print("Converted 'Game Length' to numeric values (for CS per minute):")
        print(player_df['Game Length Numeric'].head())

        # Convert 'Game Length' to human-readable format
        player_df['Game Length'] = player_df['Game Length Numeric'].apply(convert_duration)
    else:
        st.write("No 'Game Length' column found for conversion!")

    # Calculate KDA and CS per minute
    player_df = calculate_kda_and_cs(player_df)

    # Ensure that KDA and CS_per_Minute are in the column order after calculation
    if 'KDA' not in player_df.columns:
        player_df['KDA'] = 0  # Default value if the column doesn't exist
    if 'CS_per_Minute' not in player_df.columns:
        player_df['CS_per_Minute'] = 0  # Default value if the column doesn't exist

    # Add calculated columns to the column order if not already there
    if 'KDA' not in column_order:
        column_order.append('KDA')
    if 'CS_per_Minute' not in column_order:
        column_order.append('CS_per_Minute')

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
        ['Kills', 'Deaths', 'Assists', 'KDA', 'CS_per_Minute'], 
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
