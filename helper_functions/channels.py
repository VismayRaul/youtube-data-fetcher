import os
import requests
from dotenv import load_dotenv

from constant import BASE_URL, SEARCH_ENDPOINT, SNIPPET, CHANNEL

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_id(channel_handle):
    """
    Fetch the channel ID for a given YouTube channel handle using the search endpoint.
    """
    # Strip "@" from the handle if present
    clean_handle = channel_handle.lstrip("@")

    url = f"{BASE_URL}/{SEARCH_ENDPOINT}"
    params = {
        "part": SNIPPET,
        "q": clean_handle,  # Use the handle as a search query
        "type": CHANNEL,
        "key": YOUTUBE_API_KEY,
    }

    try:
        # Send the request to YouTube Data API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if "items" in data and data["items"]:
                channel_id = data["items"][0][SNIPPET]["channelId"]
                return channel_id
            else:
                print(f"No channel found for handle: {channel_handle}")
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
