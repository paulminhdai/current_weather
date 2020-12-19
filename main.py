import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
load_dotenv(verbose=True)
API_KEY = os.getenv('API_KEY')


@app.route('/', methods=['POST', 'GET'])
def render_results():
    init_zip = 90001
    message = ""

    if request.method == 'POST':
        zip_code = request.form['zipCode']
        if check_valid_zip(zip_code):
            data = get_weather_results(zip_code, API_KEY)
        else:
            data = get_weather_results(init_zip, API_KEY)
            message += "{} is not a valid zip code.".format(zip_code)
    else:
        data = get_weather_results(init_zip, API_KEY)

    date = datetime.now()
    today = date.strftime("%A %B %d %Y")

    temp = "{0:.1f}°F".format(data["main"]["temp"])
    hilow = "{0:.0f}°F - {0:.0f}°F".format(data["main"]["temp_min"], data["main"]["temp_max"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    print(temp, hilow, weather, location)

    return render_template('main.html', location=location, temp=temp,
                           hilow=hilow, weather=weather, date=today, message=message)


def check_valid_zip(zip_code):
    print("here.....")
    code = int(zip_code)
    if 500 < code < 99950:
        return True
    return False


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    res = requests.get(api_url)
    return res.json()


if __name__ == '__main__':
    app.run(host="localhost", port=8080, threaded=True, debug=True)
