import os
import shutil
import time
import streamlit as st
from config import ROFL_DIRECTORY, PROCESSED_DIRECTORY

# Save the uploaded ROFL file
def save_uploaded_file(uploaded_file):
    if not os.path.exists(ROFL_DIRECTORY):
        os.makedirs(ROFL_DIRECTORY)

    uploaded_file_path = os.path.join(ROFL_DIRECTORY, uploaded_file.name)
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file_path

# Retry logic for moving files safely
def safe_move_file(src, dest, retries=3, delay=1):
    for attempt in range(retries):
        try:
            if os.path.exists(dest):
                return True
            shutil.move(src, dest)
            return True
        except Exception as e:
            time.sleep(delay)

    return os.path.exists(dest)

# Ensure the processed file directory exists
def move_processed_file(rofl_file_path, rofl_file):
    processed_file_path = os.path.join(PROCESSED_DIRECTORY, rofl_file)
    if not os.path.exists(PROCESSED_DIRECTORY):
        os.makedirs(PROCESSED_DIRECTORY)
    return safe_move_file(rofl_file_path, processed_file_path)
