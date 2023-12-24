from django.shortcuts import render

from django.http import HttpResponseBadRequest, JsonResponse

from collections import defaultdict
from collections.abc import Iterable

def home(request):
    return render(request, "snclassifier_djangoapp/home.html")

def about(request):
    return render(request, "snclassifier_djangoapp/about.html")

def contact(request):
    return render(request, "snclassifier_djangoapp/contact.html")

from .parser.parser import InvalidYoutubeLink, get_video_comments
from snclassifier_djangoapp.predictions.get_youtube_predictions import YouTubePredictor
from django.views.decorators.csrf import csrf_exempt
import json
predictor = YouTubePredictor()

def index(request):
    return render(request, 'snclassifier_djangoapp/classifier.html')

@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data['user_input']

        # Process user_input here
        try:
            comments = get_video_comments(user_input)
            comments = predictor.get_youtube_predictions(comments)
        except InvalidYoutubeLink as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Using defaultdict for storaging comments depending on predictions
        comment_dict = defaultdict(list)

        for index, row in comments.iterrows():
            comment = row['Comment']
            prediction = row['Predictions']
            comment_dict[prediction].append(comment)

        common_lists_length = sum(len(comment_list) for comment_list in comment_dict.values())

        # Используем dictionary comprehension для вычисления процентов
        percentages = {key: round(len(comment_list) / common_lists_length * 100, 1) for key, comment_list in comment_dict.items()}

        # Добавим проценты в словарь
        comment_dict['percentages'] = percentages

        return JsonResponse(comment_dict, safe=False)
