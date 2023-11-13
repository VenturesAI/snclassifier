from django.urls import path
from snclassifier_djangoapp import views

# home_list_view = views.HomeListView.as_view(
#     queryset=LogMessage.objects.order_by("-log_date")[:5],
#     context_object_name="message_list",
#     template_name="snclassifier_djangoapp/home.html",
# )

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("process_data/", views.process_data, name="process_data"),
]