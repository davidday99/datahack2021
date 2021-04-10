from textgenrnn import textgenrnn
import pandas as pd
import re

def get_review(genre='rock'):
    if genre not in ['rock', 'electronic', 'rap', 'folk/country', 'pop']:
        genre = 'general'
    model = textgenrnn(f'{genre}.hdf5')
    text = model.generate(n=1, return_as_list=True)
    return text[0]

