import os
import requests
from dotenv import load_dotenv

from constant import BASE_URL, COMMENT_THREAD_ENDPOINT, ID, COMMENT_MAX_RESULTS_COUNT, SNIPPET

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_comments_data(video_id):
    """
    Fetch the latest 100 comments for a given video ID.
    """
    url = f"{BASE_URL}/{COMMENT_THREAD_ENDPOINT}"
    params = {
        "part": SNIPPET,
        "videoId": video_id,
        "maxResults": COMMENT_MAX_RESULTS_COUNT,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    comments = []
    
    try:
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                comment_id = item[ID]
                comment_text = item[SNIPPET]["topLevelComment"][SNIPPET]["textDisplay"]
                author_name = item[SNIPPET]["topLevelComment"][SNIPPET]["authorDisplayName"]
                published_date = item[SNIPPET]["topLevelComment"][SNIPPET]["publishedAt"]
                like_count = item[SNIPPET]["topLevelComment"][SNIPPET]["likeCount"]
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
                        reply_id = reply[ID]
                        reply_text = reply[SNIPPET]["textDisplay"]
                        reply_author = reply[SNIPPET]["authorDisplayName"]
                        reply_published = reply[SNIPPET]["publishedAt"]
                        reply_like_count = reply[SNIPPET]["likeCount"]
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
