from django.urls import path
from snclassifier_djangoapp import views
from .models import LogMessage, YoutubeComent

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],
    context_object_name="message_list",
    template_name="snclassifier_djangoapp/home.html",
)

youtube_comments_list_view = views.HomeListView.as_view(
    queryset=YoutubeComent.objects.order_by("-video_link")[:30],
    context_object_name="comments_list",
    template_name="snclassifier_djangoapp/youtube_comments.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
    path("comments/", youtube_comments_list_view, name="comments"),
]