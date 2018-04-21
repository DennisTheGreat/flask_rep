import json
import requests
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if city:
        return json.dumps(ws.current(city))
    return "Please, enter city"

class DarkSkyWeather:
    url = 'https://api.darksky.net/forecast/{api_key}/{coordinator}'
    params = None
    api_key = None
    city_map = (('Odessa', '46.4736019,30.603976'),)

    def exclude_params(self):
        self.params = {'exclude': 'currently, minutely, hourly'}

    def set_api_key(self, api_key):
        self.api_key = api_key


    def url_formatting(self,city):
        self.url = self.url.format(api_key=self.api_key, coordinator=dict(self.city_map).get(city))

    def response_content(self, city):
        self.exclude_params()
        self.url_formatting(city)
        response = requests.get(self.url, self.params)
        return json.loads(response.content)

    def current(self, city):
        result = self.response_content(city)
        return result


ws = DarkSkyWeather()
ws.set_api_key('f210178070911839dd264c60fab2dfcf')
ws.current('Odessa')


