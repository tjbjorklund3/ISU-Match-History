# Player Dashboard/column_mapping.py

# Column labels for renaming
column_labels = {
    'matchID': 'Match ID',
    'gameDuration': 'Game Length',
    'CHAMPIONS_KILLED': 'Kills',
    'NUM_DEATHS': 'Deaths',
    'ASSISTS': 'Assists',
    'NAME': 'Player',
    'SKIN': 'Champion',
    'TEAM_POSITION': 'Position',
    'WIN': 'WIN',  # Keep this as WIN for conditional formatting
    'CS_per_Minute': 'CSPM',
    'GOLD_EARNED': 'Gold',
    'MAGIC_DAMAGE_DEALT_TO_CHAMPIONS': 'Magic Damage',
    'PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS': 'Physical Damage',
    'TRUE_DAMAGE_DEALT_TO_CHAMPIONS': 'True Damage',
    'VISION_WARDS_BOUGHT_IN_GAME': 'Control Wards',
    # Add more mappings as necessary
}

# Order in which columns should be displayed
column_order = [
    'Champion',
    'Kills',
    'Deaths',
    'Assists',
    'KDA',
    'Game Length',
    'Gold',
    'CSPM',
    'WIN', 
    'Player',
    'Position',
    'Match ID', 
    'Control Wards'
]

def rename_columns(df):
    """Renames dataframe columns using predefined labels."""
    return df.rename(columns=column_labels)
