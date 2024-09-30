# Player Dashboard/data_processing.py

import pandas as pd

def convert_duration(ms):
    """Converts game duration from milliseconds to minutes:seconds format."""
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

def get_total_minutes(ms):
    """Converts milliseconds to total minutes."""
    return ms / 1000 / 60 if pd.notna(ms) else 0

def calculate_kda_and_cs(df):
    """Calculates KDA and CS per minute for a given dataframe."""
    kills_col = 'Kills'
    deaths_col = 'Deaths'
    assists_col = 'Assists'
    cs_col = 'Missions_CreepScore'
    game_duration_col = 'Game Length'

    df['KDA'] = df.apply(
        lambda row: round((row[kills_col] + row[assists_col]) / row[deaths_col], 2) 
                    if row[deaths_col] > 0 else (row[kills_col] + row[assists_col]), 
        axis=1
    )

    df['CSPM'] = df.apply(
        lambda row: round(row[cs_col] / get_total_minutes(row[game_duration_col]), 1)
                    if get_total_minutes(row[game_duration_col]) > 0 else 0,
        axis=1
    )

    return df
