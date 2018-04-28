from datetime import datetime


class Forecast:
    def __init__(self, timestamp, temperature):
        self.temperature = temperature
        self.timestamp = timestamp

    @property
    def datetime(self):
        forecast_date = datetime.fromtimestamp(self.timestamp)
        return forecast_date.strftime("%a %d %b %Y %H:%M:%S")

    @property
    def celsius_temperature(self):
        return round((self.temperature - 32) * 5/9, 2)

    def __str__(self):
        return "{} - {}".format(str(self.datetime), str(self.celsius_temperature))
