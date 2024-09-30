import os
import time
import config
import shutil
from ROFL_Upload.ROFL_To_Json import process_rofl_file
from ROFL_Upload.file_manager import move_processed_file
from config import ROFL_DIRECTORY, JSON_DIRECTORY


def safe_move_file(src, dest, retries=3, delay=1):
    """
    Attempt to move a file with retries in case of failure.
    :param src: Source file path.
    :param dest: Destination file path.
    :param retries: Number of retries in case of failure.
    :param delay: Delay between retries in seconds.
    :return: True if file moved successfully, False otherwise.
    """
    for attempt in range(retries):
        try:
            # Check if the file has already been moved
            if os.path.exists(dest):
                print(f"File {src} has already been moved to {dest}. Skipping move.")
                return True

            shutil.move(src, dest)
            print(f"Successfully moved {src} to {dest} on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} to move {src} failed: {e}")
            time.sleep(delay)

    # Final check: If file has been moved after retries, log success
    if os.path.exists(dest):
        print(f"File {src} was successfully moved to {dest} after retries.")
        return True

    print(f"Failed to move file {src} after {retries} attempts.")
    return False


# Process any ROFL files in the ROFL_DIRECTORY and include Event and Playoffs
def process_rofl_files(uploaded_file_path, selected_event, is_playoffs, latest_versions):
    rofl_files = [f for f in os.listdir(config.ROFL_DIRECTORY) if f.endswith('.rofl')]

    for rofl_file in rofl_files:
        rofl_file_path = os.path.join(config.ROFL_DIRECTORY, rofl_file)
        match_id = rofl_file.split('.')[0]

        json_output_path = os.path.join(config.JSON_DIRECTORY, f"{match_id}.json")

        if not os.path.exists(config.JSON_DIRECTORY):
            os.makedirs(config.JSON_DIRECTORY)

        # Process the ROFL file and generate the JSON, including event and playoffs data
        process_rofl_file(rofl_file_path, json_output_path, match_id, latest_versions, selected_event, is_playoffs)

        # Add a small delay before moving the processed file
        time.sleep(1)  # Wait 1 second to ensure file is fully ready to be moved

        # Move the processed ROFL file to the PROCESSED_DIRECTORY using safe move logic
        processed_file_path = os.path.join(config.PROCESSED_DIRECTORY, rofl_file)
        if not os.path.exists(config.PROCESSED_DIRECTORY):
            os.makedirs(config.PROCESSED_DIRECTORY)

        if safe_move_file(rofl_file_path, processed_file_path):
            continue
        else:
            print(f"Failed to move {rofl_file} after multiple attempts.")