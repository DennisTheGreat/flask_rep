from app import app
from flask import request
from dark_sky_api import DarkSky
from utils import login_required
from flask import session
from models import Users


@app.route('/w/')
@login_required(session)
def dark_sky_new():
    city = request.args.get('city')
    params = request.args.get('params')
    units = request.args.get('units')
    weather = DarkSky()
    weather.set_api_key('1f59ae2ad5dbb81ba6fea2a20c2f5db5')
    weather.set_api_params(params)
    weather.set_locate(city)
    weather.set_units(units)
    return weather.get_response()