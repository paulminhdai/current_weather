import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from datetime import datetime
import re

app = Flask(__name__)
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')


@app.route('/', methods=['POST', 'GET'])
def render_main_page():
    init_zip = 90001
    message = ""

    if request.method != 'POST':
        data = call_api(init_zip, API_KEY)
    else:
        zip_code = request.form['zipCode']
        data = call_api(zip_code, API_KEY)
        if not valid_api_return(data):
            data = call_api(init_zip, API_KEY)
            message += "{} is not a valid zip code.".format(zip_code)

    date = datetime.now()
    today = date.strftime("%A %B %d %Y")
    print(data)
    temp = "{0:.1f}°F".format(data["main"]["temp"])
    low = "{0:.0f}°F".format(data["main"]["temp_min"])
    high = "{0:.0f}°F".format(data["main"]["temp_max"])
    weather = data["weather"][0]["main"]
    description = data["weather"][0]["description"]
    city_name = data["name"]
    icon_link = "http://openweathermap.org/img/wn/{}.png".format(data["weather"][0]["icon"])

    return render_template('main.html', city_name=city_name, temp=temp, high=high, low=low, date=today,
                           weather=weather, description=description, icon_link=icon_link, message=message)


def valid_api_return(data):
    if data["cod"] == 200:
        return True
    return False


def call_api(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    res = requests.get(api_url)
    return res.json()


if __name__ == '__main__':
    app.run(host="localhost", port=8080, threaded=True, debug=True)
