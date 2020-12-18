import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')


@app.route('/a')
def render_home():
    return render_template("home.html")


@app.route('/')
def render_results():
    #zip_code = request.form['zipCode']
    data = get_weather_results(90703, API_KEY)

    date = datetime.now()
    today = date.strftime("%A %B %d %Y")

    temp = "{0:.1f}°F".format(data["main"]["temp"])
    hilow = "{0:.1f}°F - {0:.1f}°F".format(data["main"]["temp_min"], data["main"]["temp_max"])
    weather = data["weather"][0]["main"]
    descript = data["weather"][0]["description"]
    location = data["name"]
    print(temp, hilow, weather, location, descript)

    return render_template('main.html', location=location, temp=temp,
                           hilow=hilow, weather=weather, date=today, detail=descript)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run(host="localhost", port=8080, threaded=True, debug=True)
