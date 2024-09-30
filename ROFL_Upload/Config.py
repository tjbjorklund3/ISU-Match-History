import os

# Define where the .rofl files should be saved
ROFL_UPLOAD_DIR = os.path.join(os.getcwd(), "ROFL_Upload")

# Ensure the directory exists
if not os.path.exists(ROFL_UPLOAD_DIR):
    os.makedirs(ROFL_UPLOAD_DIR)
