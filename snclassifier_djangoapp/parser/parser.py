from googleapiclient.discovery import build
import re
import pandas as pd
from decouple import config

class InvalidYoutubeLink(Exception):
    pass

def get_video_comments(youtube_link, max_comments=100):
    # Extract the video ID from the YouTube link
    if 'youtube.com' in youtube_link:
        # Link for Web version
        video_id = youtube_link.split('=')[-1]
    elif 'youtu.be' in youtube_link:
        # Link for Mibile version
        video_id = youtube_link.split('/')[-1].split('?')[0]
    else:
        # Other links
        raise InvalidYoutubeLink("Invalid YouTube link format")

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