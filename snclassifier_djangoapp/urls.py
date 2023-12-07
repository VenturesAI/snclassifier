from django.urls import path
from snclassifier_djangoapp import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("process_data/", views.process_data, name="process_data"),
]