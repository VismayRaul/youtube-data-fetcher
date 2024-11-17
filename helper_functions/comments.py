import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = os.getenv("BASE_URL")

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
    
    try:
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
        else:
            print(f"Error fetching comments data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"An error occurred while fetching comments data: {e}")
    return comments
