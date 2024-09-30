# Player Dashboard/data_loading.py

import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Loads data from CSV file."""
    df = pd.read_csv('aggregated_replays_data.csv')
    return df

def save_data(df):
    """Saves the updated data back to the CSV file."""
    df.to_csv('aggregated_replays_data.csv', index=False)
    st.success("Changes saved successfully!")

# Normalization function to standardize player names
def normalize_string(s):
    return str(s).strip().lower()
