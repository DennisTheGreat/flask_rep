import json
from urllib.parse import urljoin

import requests


class GeoProvider:
    city_coordinates = {
                        "odessa": (46.4736019, 30.603976)
                        }

class DarkSkyWeather:
    api_key = None
    api_url = 'https://api.darksky.net'
    # url = None

    @staticmethod
    def set_api_key(key_value):
        if not key_value:
            raise ValueError("Invalid key value")
        DarkSkyWeather.api_key = key_value

    @staticmethod
    def currently(city):
        if not city:
            return "Please specify City"

        params = {'exclude': 'daily,minutely,hourly,flags'}
        response = DarkSkyWeather.__get_execute(params, city=city)
        result = json.loads(response.content.decode('utf-8'))
        return result

    @staticmethod
    def hourly(city):
        if not city:
            return "Please specify City"

        params = {'exclude': 'daily,minutely,currently,flags'}
        response = DarkSkyWeather.__get_execute(params, city=city)
        result = json.loads(response.content.decode('utf-8'))
        return result

    @staticmethod
    def daily(city):
        if not city:
            return "Please specify City"

        params = {'exclude': 'minutely,hourly,currently,flags'}
        response = DarkSkyWeather.__get_execute(params, city=city)
        result = json.loads(response.content.decode('utf-8'))
        return result

    @staticmethod
    def all(city):
        if not city:
            return "Please specify City"

        params = {'exclude': 'flags'}
        response = DarkSkyWeather.__get_execute(params, city=city)
        result = json.loads(response.content.decode('utf-8'))
        return result

    @staticmethod
    def __get_execute(params, **query_params):
        url = DarkSkyWeather.get_forecast_url(**query_params)
        response = requests.get(url, params=params)
        return response


    @staticmethod
    def get_forecast_url(**query_params):
        url_path = 'forecast/{key}/{coordinates}'

        if not DarkSkyWeather.api_key:
            raise ValueError("You should initialise api_key")

        for param_name, param_value in query_params.items():
            if param_name == "city":
                city = param_value.lower()

                if city not in GeoProvider.city_coordinates:
                    raise ValueError("Parameter {} is not a part of a coordinates dictionary.".format(city))

            url_path = url_path.format(key=DarkSkyWeather.api_key, coordinates=str(GeoProvider.city_coordinates[city])[1:-1])
        return urljoin(DarkSkyWeather.api_url, url_path)