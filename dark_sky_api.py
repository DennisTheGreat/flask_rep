import requests
import json
from datetime import datetime

class DarkSky:
    api_url = 'https://api.darksky.net/forecast/{api_key}/{coordinates}'
    api_key = None
    url = None
    params = {}
    coordinates = None

    coordinates_dict = {
                        'odessa': (46.490865, 30.7373526)
                       }

    def set_api_key(self, key_value):
        if not key_value:
            raise ImportError('U should match a key')

        if len(key_value) != 32:
            raise ValueError('Invalid key value')

        self.api_key = key_value

    def set_api_params(self, params):
        if params == "currently":
            self.params.update({'exclude': 'minutely,hourly,daily,alerts,flags'})

        elif params == "minutely":
            self.params.update({'exclude': 'currently,hourly,daily,alerts,flags'})

        elif params == "hourly":
            self.params.update({'exclude': 'currently,minutely,daily,alerts,flags'})

        elif params == "daily":
            self.params.update({'exclude': 'currently,minutely,hourly,alerts,flags'})

    def set_units(self, units):
        self.params.update({'units': units})

    def set_locate(self, locate):
        if locate in self.coordinates_dict.keys():
            self.coordinates = f'{self.coordinates_dict.get(locate)[0]},{self.coordinates_dict.get(locate)[1]}'

        elif locate[0].isdigit:
            self.coordinates = locate

    def get_response(self):
        if self.api_key is None:
            raise ImportError('U should match a key')

        if self.coordinates is None:
            raise ImportError('U should match a locate')

        self.url = f'https://api.darksky.net/forecast/{self.api_key}/{self.coordinates}'
        response = requests.get(self.url, params=self.params)
        response_content = json.loads(response.content)
        # time = datetime.fromtimestamp(((response_content.get('currently')).get('time'))).strftime('%Y-%m-%d %H:%M')
        return str(response_content)
