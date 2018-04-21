import json
import requests
from flask import Flask
app = Flask(__name__)


class DarkSkyWeather:
    url = 'https://api.darksky.net/forecast/{api_key}/{coordinates}'
    params = {}
    api_key = None
    city = None
    city_map = {'odessa': '46.4736019,30.603976'}

    def __init__(self, api_key, city='odessa', params='currently,minutely,hourly'):
        self.__check_city(city)
        self.set_api_key(api_key)
        self.city = city
        self.__check_params(params)

    def set_api_key(self, api_key):
        self.api_key = api_key

    def execute_request(self, api_key, coordinates, params):
        url = self.url.format(api_key=api_key, coordinates=coordinates)
        response = requests.get(url, params=params)
        return response

    def __check_city(self, city):
        assert self.city_map.get(city) is not None, 'No such city in list!'

    def __check_params(self, params):
        if len(str(params)) > 0:
            self.params = {'exclude': params}
        else:
            self.params = {}

    def current(self, city_name):
        assert self.city_map[city_name]
        api_key = self.api_key
        params = {'exclude': 'currently,minutely,hourly'}
        coordinates = self.city_map[city_name]
        return self.execute_request(api_key, coordinates, params)


@app.route('/weather/<city_name>/')
def get_weather(city_name):
    api_key = '34923e111f832447d27c4c02dfe7e813'
    # params_to_exclude = 'currently,minutely,hourly'
    weather_request = DarkSkyWeather(api_key)
    response = weather_request.current(city_name)
    response_content = json.loads(response.content)
    return json.dumps(response_content)

