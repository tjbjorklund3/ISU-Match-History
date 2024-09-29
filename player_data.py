import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import JsCode  # For custom JS code injection
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

# Convert gameDuration from milliseconds to minutes:seconds format without leading zeros
def convert_duration(ms):
    if pd.isna(ms):
        return "00:00"
    seconds = ms // 1000
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes)}:{int(seconds):02d}"

# Convert gameDuration from milliseconds to total minutes
def get_total_minutes(ms):
    return ms / 1000 / 60 if pd.notna(ms) else 0

# Calculate KDA and CS per minute
def calculate_kda_and_cs(df):
    kills_col = 'Kills'  # Confirmed key from your provided list
    deaths_col = 'Deaths'       # Confirmed key
    assists_col = 'Assists'         # Confirmed key
    cs_col = 'Missions_CreepScore'  # Confirmed key
    game_duration_col = 'Game Length'  # Confirmed key

    # Calculate KDA: (Kills + Assists) / Deaths (if Deaths > 0)
    df['KDA'] = df.apply(lambda row: round((row[kills_col] + row[assists_col]) / row[deaths_col], 2) if row[deaths_col] > 0 else (row[kills_col] + row[assists_col]), axis=1)

    # Calculate CS per minute: Missions_CreepScore / game length (in minutes)
    df['CSPM'] = df.apply(lambda row: round(row[cs_col] / get_total_minutes(row[game_duration_col]), 1) if get_total_minutes(row[game_duration_col]) > 0 else 0, axis=1)

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

    # Calculate KDA and CS per minute
    player_df = calculate_kda_and_cs(player_df)

    # Convert game duration from ms to a readable format
    if 'Game Length' in player_df.columns:
        player_df['Game Length'] = player_df['Game Length'].apply(convert_duration)

    # Ensure that KDA and CS_per_Minute (CSPM) are in the column order after calculation
    if 'KDA' not in column_order:
        column_order.append('KDA')
    if 'CSPM' not in column_order:
        column_order.append('CSPM')
    if 'WIN' not in column_order:
        column_order.append('WIN')
    if 'Match ID' in column_order:
        column_order.remove('Match ID')
        column_order.append('Match ID')

    # Reorder columns as per the new column_order
    player_df = player_df[column_order]

    # Inject custom JavaScript code for row coloring based on 'WIN' column using hex color codes
    cellStyle = JsCode("""
        function(params) {
            if (params.data.WIN == 'Win') {
                return {'backgroundColor': '#b6e7a2'};  // Custom light green hex color
            } else if (params.data.WIN == 'Fail') {
                return {'backgroundColor': '#f08080'};  // Custom light red hex color
            }
            return {};
        }
    """)

    # Configure grid options for AgGrid
    gb = GridOptionsBuilder.from_dataframe(player_df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Pagination for large datasets
    gb.configure_side_bar()  # Enable sidebar filters
    gb.configure_default_column(editable=True, filter=True, resizable=True)  # Columns are editable and filterable
    gb.configure_grid_options(domLayout='autoHeight')  # Automatically adjusts height of the grid

    # Set custom column widths if needed (Optional)
    gb.configure_columns(
        ['Kills', 'Deaths', 'Assists', 'KDA', 'CSPM', 'Gold'], 
        width=80  # Example: Adjust width of these columns
    )

    # Fit all columns except "Player" and "Match ID"
    gb.configure_columns(['Player', 'Match ID'], width=60)

    # Apply the custom cell style for row coloring
    gridOptions = gb.build()
    gridOptions['defaultColDef']['cellStyle'] = cellStyle

    # Display the editable table using AgGrid
    grid_response = AgGrid(
        player_df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=True,
        theme="streamlit",  # Theme: balham, material, etc.
        allow_unsafe_jscode=True,  # Allow JavaScript code execution
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
