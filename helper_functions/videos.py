import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = os.getenv("BASE_URL")

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
