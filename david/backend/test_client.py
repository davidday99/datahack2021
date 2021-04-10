import requests

X_test = [.24, 4, 175.9, 32, 1.2, 1.06, 388200, 8, -0.676, 'major', 'rock', 'C#', 'NOT VULGAR', 'Juans Song', 'Juan', 'Juans Album']
param_names = ['auditory', 'beats_per_measure', 'beats_per_min', 'concert_probability',
       'danceability', 'instrumentalness', 'length_minutes', 'lyricism',
       'positivity', 'major/minor', 'styles', 'tone', 'vulgar', 'name', 'artist', 'album']


params = {}
for idx in range(len(param_names)):
    params[param_names[idx]] = X_test[idx]

print(params)

response = requests.get("http://127.0.0.1:5000/api/model", params=params)
print(response.text)