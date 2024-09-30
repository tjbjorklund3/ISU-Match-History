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
}

# Order in which columns should be displayed
column_order = [
    'Champion',
    'Position',
    'Game Length',
    'Kills',
    'Deaths',
    'Assists',
    'KDA',
    'CSPM',
    'Gold',
    'Damage Profile',  # Add the calculated damage profile bar
    'WIN',
    'Player',
    'Match ID', 
]
