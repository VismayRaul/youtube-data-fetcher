import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def get_channel_id(channel_handle):
    """
    Fetch the channel ID for a given YouTube channel handle using the search endpoint.
    """
    # Strip "@" from the handle if present
    clean_handle = channel_handle.lstrip("@")

    url = f"{BASE_URL}/search"
    params = {
        "part": "snippet",
        "q": clean_handle,  # Use the handle as a search query
        "type": "channel",
        "key": YOUTUBE_API_KEY,
    }

    try:
        # Send the request to YouTube Data API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if "items" in data and data["items"]:
                channel_id = data["items"][0]["snippet"]["channelId"]
                return channel_id
            else:
                print(f"No channel found for handle: {channel_handle}")
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_all_videos(channel_id):
    """
    Fetch all video IDs for a given channel ID.
    """
    videos = []
    url = f"{BASE_URL}/search"
    next_page_token = None

    while True:
        params = {
            "part": "id",
            "channelId": channel_id,
            "maxResults": 50,
            "type": "video",
            "pageToken": next_page_token,
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                videos.append(item["id"]["videoId"])
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
        else:
            break
    return videos

def get_video_details(video_ids):
    """
    Fetch detailed information for a list of video IDs.
    """
    video_data = []
    url = f"{BASE_URL}/videos"

    for i in range(0, len(video_ids), 50):
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids[i:i+50]),
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                snippet = item["snippet"]
                stats = item.get("statistics", {})
                content = item["contentDetails"]
                video_data.append({
                    "Video ID": item["id"],
                    "Title": snippet["title"],
                    "Description": snippet["description"],
                    "Published Date": snippet["publishedAt"],
                    "View Count": stats.get("viewCount", "0"),
                    "Like Count": stats.get("likeCount", "0"),
                    "Comment Count": stats.get("commentCount", "0"),
                    "Duration": content["duration"],
                    "Thumbnail URL": snippet["thumbnails"]["default"]["url"]
                })
    return video_data

def get_comments_data(video_id):
    """
    Fetch the latest 100 comments for a given video ID.
    """
    url = f"{BASE_URL}/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    comments = []
    
    if response.status_code == 200:
        data = response.json()
        for item in data["items"]:
            comment_id = item["id"]
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            published_date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            comments.append({
                "Comment ID": comment_id,
                "Comment Text": comment_text,
                "Author": author_name,
                "Published Date": published_date,
                "Like Count": like_count
            })
            # Check for replies
            if "replies" in item:
                for reply in item["replies"]["comments"]:
                    reply_id = reply["id"]
                    reply_text = reply["snippet"]["textDisplay"]
                    reply_author = reply["snippet"]["authorDisplayName"]
                    reply_published = reply["snippet"]["publishedAt"]
                    reply_like_count = reply["snippet"]["likeCount"]
                    comments.append({
                        "Comment ID": reply_id,
                        "Comment Text": reply_text,
                        "Author": reply_author,
                        "Published Date": reply_published,
                        "Like Count": reply_like_count,
                        "Reply to": comment_id  # Link reply to the parent comment
                    })
    return comments

def export_to_excel(video_data, comments_data):
    """
    Export video and comment data to a dynamically named Excel file in the Downloads folder.
    """
    # Determine the Downloads directory
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Create a dynamic file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"YouTube_Data_{timestamp}.xlsx"
    file_path = os.path.join(downloads_folder, file_name)

    # Write the data to the Excel file
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        # Video Data Sheet
        video_df = pd.DataFrame(video_data)
        video_df.to_excel(writer, sheet_name="Video Data", index=False)

        # Comments Data Sheet
        comments_df = pd.DataFrame(comments_data)
        comments_df.to_excel(writer, sheet_name="Comments Data", index=False)

    print(f"File has been saved to: {file_path}")
    return file_path

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
