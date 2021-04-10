from flask import Flask, request
from markupsafe import Markup
from textgenrnn import textgenrnn
import re
import pandas as pd
import numpy as np
import catboost
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import math
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import stats
from nltk.sentiment import SentimentIntensityAnalyzer


app = Flask(__name__)
model = None
scaler = None

def load_pretrained():
    global model
    model = catboost.CatBoostRegressor()
    model.load_model('catboost_regressor')

def init_model():
    # Train Catboost model to predict number of streams
    global model
    print('********* Training model... *********')
    official_competition_dataset = pd.read_csv('https://datahack2020dataset.s3.us-east-2.amazonaws.com/OfficialCompetitionDataset.csv')
    numerical_cols = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability',
                     'danceability', 'hype', 'instrumentalness', 'length_minutes',
                     'lyricism', 'nplays', 'positivity', 'volume'] # no hotness and critic rating because unlikely for amateur band
    categorical_features = ['major/minor', 'styles', 'tone', 'vulgar'] # no critic/reviewer_type/album/artist/name
    numerical_cols_no_nplays = [x for x in numerical_cols if x != 'nplays']
    y = official_competition_dataset['nplays']
    y = np.log1p(y)
    X = official_competition_dataset.drop('nplays', axis=1)
    X["reviewer_type"].fillna("contributor", inplace=True) 
    X["styles"].fillna("rock", inplace=True) 

    text_features = ['name', 'album', 'artist']
    extra_numerical_features = []
    sia = SentimentIntensityAnalyzer()
    for f in text_features:
        temp = [f'{f}_len', f'{f}_upper', f'{f}_sent_pos', f'{f}_sent_neg']
        X[f'{f}_len'] = X[f'{f}'].str.len()
        X[f'{f}_upper'] = X[f'{f}'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
        X[f'{f}_sent_pos'] = X[f'{f}'].apply(lambda x: sia.polarity_scores(x)['pos'])
        X[f'{f}_sent_neg'] = X[f'{f}'].apply(lambda x: sia.polarity_scores(x)['neg'])
        extra_numerical_features = extra_numerical_features + temp
    X.drop(text_features, axis=1, inplace=True)

    X = X[numerical_cols_no_nplays + extra_numerical_features + categorical_features]
    print(X.head())
    cor_matrix = X.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.5)]
    print(to_drop)
    numerical_cols_no_nplays_no_highly_correlated_features = [x for x in numerical_cols_no_nplays if x not in to_drop]
    X = X.drop(to_drop, axis=1)
    print(X.head())
    print(X.columns)
    print(list(X.iloc[0]))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    global scaler
    scaler = MinMaxScaler()
    X_train[numerical_cols_no_nplays_no_highly_correlated_features] = scaler.fit_transform(X_train[numerical_cols_no_nplays_no_highly_correlated_features])
    X_test[numerical_cols_no_nplays_no_highly_correlated_features] = scaler.transform(X_test[numerical_cols_no_nplays_no_highly_correlated_features])
    print("**********************")
    print(numerical_cols_no_nplays_no_highly_correlated_features)

    model = catboost.CatBoostRegressor(depth=10, l2_leaf_reg=5, learning_rate=0.1, cat_features=categorical_features, logging_level="Silent")
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    n = X_test.shape[0]
    p = X_test.shape[1]
    r2 = r2_score(y_test, pred)
    print('r2 score: ', r2)
    print('adjusted r2 score: ', 1-(1-r2)*(n-1)/(n-p-1))
    print('root mean squared error: ', math.sqrt(mean_squared_error(y_test, pred)))
    print('mean absolute error: ', mean_absolute_error(y_test, pred))
    model.save_model('catboost_regressor')

def feature_engineering(param_dict):
    desired_param_names = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability',
       'danceability', 'instrumentalness', 'length_minutes', 'lyricism',
       'positivity', 'name_len', 'name_upper', 'name_sent_pos',
       'name_sent_neg', 'album_len', 'album_upper', 'album_sent_pos',
       'album_sent_neg', 'artist_len', 'artist_upper', 'artist_sent_pos',
       'artist_sent_neg', 'major/minor', 'styles', 'tone', 'vulgar']

    features = []

    ## Append engineered features to dictionary
    numerical_cols = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability', 'danceability', 'instrumentalness', 'length_minutes', 'lyricism', 'positivity']
    categorical_features = ['major/minor', 'styles', 'tone', 'vulgar']
    text_features = ['name', 'album', 'artist']
    sia = SentimentIntensityAnalyzer()
    for f in text_features:
        temp = [f'{f}_len', f'{f}_upper', f'{f}_sent_pos', f'{f}_sent_neg']
        param_dict[f'{f}_len'] = len(param_dict[f'{f}'])
        param_dict[f'{f}_upper'] = len([x for x in param_dict[f'{f}'].split() if x.isupper()])
        param_dict[f'{f}_sent_pos'] = sia.polarity_scores(param_dict[f'{f}'])['pos']
        param_dict[f'{f}_sent_neg'] = sia.polarity_scores(param_dict[f'{f}'])['neg']

    unscaled_features = []
    for f in numerical_cols:
        unscaled_features.append(param_dict[f])

    unscaled_features = np.array(unscaled_features)
    unscaled_features.reshape(1, -1)
    global scaler
    scaled_features = scaler.transform(unscaled_features)
    for f in numerical_cols:
        param_dict[f] = scaled_features

    for param in desired_param_names:
        features.append(param_dict[param])

    return features


def get_review(name, album, artist, genre='rock'):
    if genre not in ['rock', 'electronic', 'rap', 'folk/country', 'pop']:
        genre = 'general'
    model = textgenrnn(f'{genre}.hdf5')
    text = model.generate(n=1, return_as_list=True)[0]
    text = re.sub('album', album, text)
    text = re.sub('name', name, text)
    text = re.sub('artist', artist, text)
    return text

def get_prediction(X_test):
    global model
    y_pred = model.predict(X_test)
    return int(np.expm1(y_pred))


@app.route('/')
def index():
    return Markup('<h1>Test</h1>')


# Front-end will send a form with all the data filled out.
# Use the data to make a prediction and return it to the front-end.
@app.route('/api/model', methods=['GET', 'POST'])
def predict_and_review():
    # desired_param_names = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability',
    #    'danceability', 'instrumentalness', 'length_minutes', 'lyricism',
    #    'positivity', 'name_len', 'name_upper', 'name_sent_pos',
    #    'name_sent_neg', 'album_len', 'album_upper', 'album_sent_pos',
    #    'album_sent_neg', 'artist_len', 'artist_upper', 'artist_sent_pos',
    #    'artist_sent_neg', 'major/minor', 'styles', 'tone', 'vulgar']

    # param_names = ['artistName','songName','albumName','beatsPerMeasure','beatsPerMinute','lengthInMinutes',
    #                 'lengthInMinutes','lyricism', 'volume', 'danceability', 'positivity', 'hype', 
    #                 'instrumentalness', 'majorMinor', 'vulgarity', 'concertProbability', 'auditory', 'tone']

    param_names = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability',
       'danceability', 'instrumentalness', 'length_minutes', 'lyricism',
       'positivity', 'major/minor', 'styles', 'tone', 'vulgar', 'name', 'artist', 'album']

    param_dict = {}
    param_list = []
    for param in param_names:
        param_dict[param] = request.args.get(param)
        param_list.append(request.args.get(param))

    print(param_dict)

    features = feature_engineering(param_dict)

    prediction = get_prediction(param_list)
    genre = param_dict['styles'].split()[0]
    review = get_review(param_dict['name'], param_dict['album'], param_dict['artist'], genre)
    return f'{prediction}, {review}'

if __name__ == '__main__':
    app.debug = True
    pretrained = False
    if pretrained:
        load_pretrained()
    else:
        init_model()
    # X_test = [.24, 4, 175.9, 32, 1.2, 1.06, 388200, 8, -0.676, 43, 1, 0, 0.241, 2, 1, 0, 0, 18, 0, 0.607, 0, 'major', 'rock', 'C#', 'NOT VULGAR']
    # print('MAKING PREDICTION')
    # print(get_prediction(X_test))
    # print(get_review('Hello, World', 'My Sick Album', 'The Killers', 'rock'))
    app.run()
