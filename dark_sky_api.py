import requests
import json

class DarkSky:
    api_url = 'https://api.darksky.net/forecast/{api_key}/{coordinates}'
    api_key = None
    url = None
    params = None
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
            self.params = {'exclude': 'minutely,hourly,daily'}

        if params == "minutely":
            self.params = {'exclude': 'currently,hourly,daily'}

        if params == "hourly":
            self.params = {'exclude': 'currently,minutely,daily'}

        if params == "daily":
            self.params = {'exclude': 'currently,minutely,hourly'}

        # else:
        #     raise ValueError('Invalid key value')

    def set_locate(self, locate):
        if locate in self.coordinates_dict.keys():
            self.coordinates = f'{self.coordinates_dict.get(locate)[0]},{self.coordinates_dict.get(locate)[1]}'

        if isinstance(locate, tuple):
            self.coordinates = f'{locate[0]},{locate[1]}'

    def get_response(self):
        if self.api_key is None:
            raise ImportError('U should match a key')

        if self.params is None:
            raise ImportError('U should match params')

        if self.coordinates is None:
            raise ImportError('U should match a locate')

        self.url = f'https://api.darksky.net/forecast/{self.api_key}/{self.coordinates}'
        response = requests.get(self.url, params=self.params)
        response_content = json.loads(response.content)
        return json.dumps(response_content)
