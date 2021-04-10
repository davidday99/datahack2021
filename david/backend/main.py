from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


@app.route('/')
def index():
    return Markup('<h1>Test</h1>')


# Front-end will send a form with all the data filled out.
# Use the data to make a prediction and return it to the front-end.
@app.route('/api/model1', methods=['POST'])
def get_prediction():
    value1 = request.form['value1']
    print(value1)
    return value1  # echo back the value posted


if __name__ == '__main__':
    app.run()
