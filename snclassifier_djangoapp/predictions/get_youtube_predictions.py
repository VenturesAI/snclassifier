#Here you will find method get_youtube_predictions(comments) which requires as imput pandas DataFrame with column "Comment".
#As output you will get tensor with predictions, where 0 - negative comment, 1 - neutral, 2 -positive.

from fastai.text.all import *
import pandas as pd
from langdetect import detect
import re

class YouTubePredictor:
    def __init__(self, model_path='backend/predictions/saved_ml_models/ULMFiT_model.pkl'):
        # Load the model during initialization
        self.learn = load_learner(model_path)

    def preprocess_data(self, df):
        #delete empty rows
        df = df.dropna().drop_duplicates()
        df["Comment"] = df["Comment"].str.lower()

        # Vectorized cleaning
        df["Comment"] = df["Comment"].str.replace(r'#\w+', '').str.replace(r'http\S+', '').str.replace(r'@\w+', '')

        # Defining list of Abbreviations to be expanded to its original form
        abbreviations = {'fyi': 'for your information',
                    'lol': 'laugh out loud',
                    'loza': 'laughs out loud',
                    'lmao': 'laughing',
                    'rofl': 'rolling on the floor laughing',
                    'vbg': 'very big grin',
                    'xoxo': 'hugs and kisses',
                    'xo': 'hugs and kisses',
                    'brb': 'be right back',
                    'tyt': 'take your time',
                    'thx': 'thanks',
                    'abt': 'about',
                    'bf': 'best friend',
                    'diy': 'do it yourself',
                    'faq': 'frequently asked questions',
                    'fb': 'facebook',
                    'idk': 'i don\'t know',
                    'asap': 'as soon as possible',
                    'syl': 'see you later',
                    'nvm': 'never mind',
                    'frfr':'for real for real',
                    'istg':'i swear to god',}


        for short_form, full_form in abbreviations.items(): # Expanding the Abbreviations
            df["Comment"] = df["Comment"].str.replace(short_form, full_form)
        return df

    def get_youtube_predictions(self, comments):
        #preprocess imput data
        comments = self.preprocess_data(comments)
        comments = comments.sample(frac=1, random_state=42).reset_index(drop=True)

        #load input dataframe in fastai dataloader(test_dl)
        test_dl = self.learn.dls.test_dl(comments["Comment"])

        #Make prediction
        preds, _ = self.learn.get_preds(dl=test_dl)
        predicted_classes = preds.argmax(dim=1)
        comments["Predictions"] = predicted_classes.numpy()

        return comments