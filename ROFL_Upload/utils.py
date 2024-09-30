# utils.py

import requests
import config

# Function to fetch the latest Riot game versions from the API
def fetch_latest_versions():
    try:
        response = requests.get(config.RIOT_API_VERSIONS_URL)
        response.raise_for_status()
        return response.json()  # Returns a list of version strings
    except requests.RequestException as e:
        print(f'Error fetching versions from Riot API: {e}')
        return []
