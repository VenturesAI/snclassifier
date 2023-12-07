from googleapiclient.discovery import build
import re
import pandas as pd
from decouple import config

def get_video_comments(youtube_link, max_comments=300):
    # Extract the video ID from the YouTube link
    video_id = re.search(r'(?<=v=)[^&]+', youtube_link)

    if video_id:
        video_id = video_id.group(0)
    else:
        # Handle invalid or unsupported YouTube link
        return []

    API_KEY = config('API_KEY')

    # Initialize the YouTube Data API
    youtube = build('youtube', 'v3', developerKey = API_KEY)

    # Request video comments
    comments = []
    nextPageToken = None
    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part = 'snippet',
            videoId = video_id,
            textFormat = 'plainText',
            pageToken = nextPageToken
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    comments = pd.DataFrame({'Comment': comments})

    return comments