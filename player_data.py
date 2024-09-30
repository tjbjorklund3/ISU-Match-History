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

# Calculate KDA, CSPM, and add Damage Profile proportions
# Calculate KDA, CSPM, and add Damage Profile proportions
def calculate_stats(df):
    kills_col = 'Kills'
    deaths_col = 'Deaths'
    assists_col = 'Assists'
    cs_col = 'Missions_CreepScore'
    game_duration_col = 'Game Length'
    magic_dmg_col = 'Magic Damage'
    physical_dmg_col = 'Physical Damage'
    true_dmg_col = 'True Damage'

    # Calculate KDA: (Kills + Assists) / Deaths (if Deaths > 0)
    df['KDA'] = df.apply(lambda row: round((row[kills_col] + row[assists_col]) / row[deaths_col], 2) if row[deaths_col] > 0 else (row[kills_col] + row[assists_col]), axis=1)

    # Calculate CSPM: Missions_CreepScore / game length (in minutes)
    df['CSPM'] = df.apply(lambda row: round(row[cs_col] / get_total_minutes(row[game_duration_col]), 1) if get_total_minutes(row[game_duration_col]) > 0 else 0, axis=1)

    # Ensure damage columns are numeric and handle NaN values
    df[magic_dmg_col] = pd.to_numeric(df[magic_dmg_col], errors='coerce').fillna(0)
    df[physical_dmg_col] = pd.to_numeric(df[physical_dmg_col], errors='coerce').fillna(0)
    df[true_dmg_col] = pd.to_numeric(df[true_dmg_col], errors='coerce').fillna(0)

    # Calculate Damage Profile percentages
    df['Total_Damage'] = df[magic_dmg_col] + df[physical_dmg_col] + df[true_dmg_col]
    df['Magic_Damage_Perc'] = df.apply(lambda row: round(row[magic_dmg_col] / row['Total_Damage'], 2) if row['Total_Damage'] > 0 else 0, axis=1)
    df['Physical_Damage_Perc'] = df.apply(lambda row: round(row[physical_dmg_col] / row['Total_Damage'], 2) if row['Total_Damage'] > 0 else 0, axis=1)
    df['True_Damage_Perc'] = df.apply(lambda row: round(row[true_dmg_col] / row['Total_Damage'], 2) if row['Total_Damage'] > 0 else 0, axis=1)

    return df


# Rename columns for better readability
def rename_columns(df):
    return df.rename(columns=column_labels)

# Hard-coded JavaScript renderer for damage profile bar
damage_profile_renderer = JsCode("""
    function(params) {
        // Hard-code the damage percentages for testing
        let magicDamage = 20;  // 20%
        let physicalDamage = 50;  // 50%
        let trueDamage = 30;  // 30%

        return `<div style='display: flex; height: 100%;'>
                    <div style='width: ${magicDamage}%; background-color: #3498db;'></div>
                    <div style='width: ${physicalDamage}%; background-color: #e74c3c;'></div>
                    <div style='width: ${trueDamage}%; background-color: #f1c40f;'></div>
                </div>`;
    }
""")



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

    # Calculate KDA, CSPM, and damage proportions
    player_df = calculate_stats(player_df)

    # Convert game duration from ms to a readable format
    if 'Game Length' in player_df.columns:
        player_df['Game Length'] = player_df['Game Length'].apply(convert_duration)

    # Ensure new columns are in the display order
    if 'KDA' not in player_df.columns:
        player_df['KDA'] = 0
    if 'CSPM' not in player_df.columns:
        player_df['CSPM'] = 0
    if 'Damage Profile' not in player_df.columns:
        player_df['Damage Profile'] = ''
    if 'WIN' not in player_df.columns:
        player_df['WIN'] = ''

    # Reorder columns as per the new column_order
    player_df = player_df[[col for col in column_order if col in player_df.columns]]

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
    gb.configure_columns(['Player', 'Match ID'], width=120)

    # Configure the 'Damage Profile' column to use the custom renderer
    gb.configure_column('Damage Profile', cellRenderer=damage_profile_renderer)

    # Add Damage Profile column with custom renderer
    gb.configure_column('Damage Profile', cellRenderer=damage_profile_renderer)

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
