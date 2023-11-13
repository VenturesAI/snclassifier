from googleapiclient.discovery import build
import re
import pandas as pd

api_key = "AIzaSyCKXIwPV2bgtOqdn2l1RXaQmdOgMwsenyI"

def get_video_comments(youtube_link):
    print(f'youtube_link = {youtube_link}')
    # Extract the video ID from the YouTube link
    video_id = re.search(r'(?<=v=)[^&]+', youtube_link)
    print(f'video_id = {video_id}')
    if video_id:
        video_id = video_id.group(0)
    else:
        # Handle invalid or unsupported YouTube link
        return []

    # Initialize the YouTube Data API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request video comments
    comments = []
    nextPageToken = None
    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=nextPageToken
        ).execute()
        print(f"responce = {response['items']}")
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    comments = pd.DataFrame({'Comment': comments})
    print(f'comments = {comments}')
    return comments