from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

from django.utils.timezone import datetime

from django.shortcuts import redirect
from .forms import LogMessageForm
from .models import LogMessage

from django.views.generic import ListView


def home(request):
    return render(request, "snclassifier_djangoapp/home.html")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "snclassifier_djangoapp/about.html")

def contact(request):
    return render(request, "snclassifier_djangoapp/contact.html")

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "snclassifier_djangoapp/log_message.html", {"form": form})