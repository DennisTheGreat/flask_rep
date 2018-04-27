import json
import requests
from flask import Flask
from app import app


@app.route('/weather/odessa/')
def hello_world():
    url = 'https://api.darksky.net/forecast/070cb4f3ace25c5cdfedf89527ba83f6/46.4736019,30.603976'
    params = {'exclude':'currently,minutely,hourly'}
    response = requests.get(url, params=params)
    response_content = json.loads(response.content)
    return json.dumps(response_content)
