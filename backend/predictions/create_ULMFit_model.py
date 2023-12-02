#accuracy 0.835990
from fastai.text.all import *
import pandas as pd
from langdetect import detect
import re
from django.conf import settings

CSV_FILE_PATH = "/home/nds/projects/snclassifier/snclassifier/backend/predictions/datasets/comments.csv"

comments = pd.read_csv(CSV_FILE_PATH)

def preprocess_data(df):
    #delete empty rows, delete duplicates
    df = df.dropna().drop_duplicates()

    df["Comment"] = df["Comment"].str.lower()
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
    df = df.sample(frac=1, random_state=42)
    return df

comment_2 = preprocess_data(comments)
df_lm = comment_2

dls_lm = DataBlock(
    blocks=TextBlock.from_df('Comment', is_lm=True),
    get_x=ColReader('text'),splitter=RandomSplitter(0.1))
dls_lm = dls_lm.dataloaders(df_lm , bs=32, seq_len=72)

learn = language_model_learner(dls_lm, AWD_LSTM, drop_mult=0.3, metrics=[accuracy]).to_fp16()

learn.fine_tune(5, 1e-2)
learn.save_encoder('finetuned')

blocks = (TextBlock.from_df('Comment', seq_len=dls_lm.seq_len, vocab=dls_lm.vocab), CategoryBlock())
dls = DataBlock(blocks=blocks,
                get_x=ColReader('text'),
                get_y=ColReader('Sentiment'),
                splitter=RandomSplitter(0.2))

dls = dls.dataloaders(comment_2, bs=32)
dls.show_batch(max_n=3)

learn_2 = text_classifier_learner(dls, AWD_LSTM, metrics=[accuracy]).to_fp16()
learn_2.load_encoder('finetuned')

learn_2.fit_one_cycle(1, 1e-2)

# Applying gradual unfreezing of one layer after another
#learn_2.freeze_to(-2)
#learn_2.fit_one_cycle(3, slice(1e-3/(2.6**4),1e-2))

learn_2.freeze_to(-3)
learn_2.fit_one_cycle(3, slice(5e-3/(2.6**4),1e-2))

learn_2.unfreeze()
learn_2.fit_one_cycle(5, slice(1e-3/(2.6**4),3e-3))

predictions = learn_2.get_preds(dl=learn_2.dls.test_dl(comment_2["Comment"].iloc[:5], bs=32))
predicted_classes = predictions[0].argmax(dim=1)
print(predicted_classes)

learn_2.export('/home/nds/projects/snclassifier/snclassifier/backend/predictions/saved_ml_models/ULMFiT_model.pkl')