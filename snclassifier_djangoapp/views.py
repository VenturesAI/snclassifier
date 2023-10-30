from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

from django.utils.timezone import datetime, make_aware

from django.shortcuts import redirect
from .forms import LogMessageForm
from .models import LogMessage, YoutubeComent

from django.views.generic import ListView

import requests

def home(request):
    return render(request, "snclassifier_djangoapp/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context
class YoutubeCommentsListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = YoutubeComent

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def about(request):
    return render(request, "snclassifier_djangoapp/about.html")

def contact(request):
    return render(request, "snclassifier_djangoapp/contact.html")

def youtube_comments(request):
    return render(request, "snclassifier_djangoapp/youtube_comments.html")

def get_comments_from_youtube(video_id, api_key):
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
    response = requests.get(url)
    data = response.json()
    comments = []

    for item in data.get('items', []):
        top_comment = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'author': top_comment['authorDisplayName'],
            'text': top_comment['textDisplay'],
            'published_at': top_comment['publishedAt']
        })

    return comments

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            video_id = message.message.split("https://www.youtube.com/watch?v=")[-1]
            print(f"message= {message.message}")
            print(f"video_id= {video_id}")
            API_KEY = 'AIzaSyCtRterjnnJxCGDpW4IZ4OrrgL7B5SzzXg'
            comments = get_comments_from_youtube(video_id, API_KEY)
            for comment in comments:
                youtube_comment = YoutubeComent()
                youtube_comment.author = comment['author']
                youtube_comment.text = comment['text']
                youtube_comment.video_link = "https://www.youtube.com/watch?v=" + video_id

                # Convert the 'published_at' string to a datetime object before saving
                youtube_comment.date = datetime.strptime(comment['published_at'], '%Y-%m-%dT%H:%M:%SZ')
                youtube_comment.date = make_aware(youtube_comment.date)

                youtube_comment.save()

            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "snclassifier_djangoapp/log_message.html", {"form": form})

    # VIDEO_ID = '4n-lkYFqXGM'
    # API_KEY = 'AIzaSyCtRterjnnJxCGDpW4IZ4OrrgL7B5SzzXg'
    # comments = get_comments_from_youtube(VIDEO_ID, API_KEY)
    # for comment in comments:
    #     print(comment['author'], ":", comment['text'])