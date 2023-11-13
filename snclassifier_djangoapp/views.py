from django.shortcuts import render

from django.http import JsonResponse


from django.views.generic import ListView

def home(request):
    return render(request, "snclassifier_djangoapp/home.html")

def about(request):
    return render(request, "snclassifier_djangoapp/about.html")

def contact(request):
    return render(request, "snclassifier_djangoapp/contact.html")

from .parser.parser import get_video_comments
from .predictions.get_youtube_predictions import get_youtube_predictions
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'snclassifier_djangoapp/classifier.html')

@csrf_exempt
def process_data(request):
    print('process_data')
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data['user_input']

        # Process user_input here
        comments = get_video_comments(user_input)
        comments = get_youtube_predictions(comments)

        list_0 = []
        list_1 = []
        list_2 = []
        common_list = []

        # Iterate through the DataFrame and distribute comments based on "Prediction" value
        for index, row in comments.iterrows():
            comment = row['Comment']
            prediction = row['Predictions']

            if prediction == 0:
                list_0.append(comment)
            elif prediction == 1:
                list_1.append(comment)
            elif prediction == 2:
                list_2.append(comment)
        common_lists_lenght = len(list_0) + len(list_1) + len (list_2)
        procents0 = round(len(list_0)/common_lists_lenght*100, 0)
        procents1 = round(len(list_1)/common_lists_lenght*100, 0)
        procents2 = round(len(list_2)/common_lists_lenght*100, 0)
        common_list.append(list_0)
        common_list.append(list_1)
        common_list.append(list_2)
        common_list.append(procents0)
        common_list.append(procents1)
        common_list.append(procents2)

        return JsonResponse(common_list, safe=False)