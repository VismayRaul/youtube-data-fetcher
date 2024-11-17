import os
from dotenv import load_dotenv

from helper_functions.channels import get_channel_id
from helper_functions.videos import get_all_videos, get_video_details
from helper_functions.comments import get_comments_data
from helper_functions.excel_export import export_to_excel

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def main(channel_handle):
    """
    Main function to fetch YouTube data and export to Excel.
    """
    # Get the channel ID from the handle
    channel_id = get_channel_id(channel_handle)
    if not channel_id:
        print(f"Channel with handle {channel_handle} not found.")
        return

    print(f"Fetching video data for channel: {channel_handle} (ID: {channel_id})")
    video_ids = get_all_videos(channel_id)
    video_data = get_video_details(video_ids)

    all_comments_data = []
    print(f"Fetching comments data for videos in channel {channel_handle}...")
    for video in video_data:
        comments_data = get_comments_data(video["Video ID"])
        all_comments_data.extend(comments_data)

    # Export data to Excel
    export_to_excel(video_data, all_comments_data)

if __name__ == "__main__":
    channel_handle = input("Enter the YouTube channel handle (e.g., @channelhandle): ")
    main(channel_handle)
