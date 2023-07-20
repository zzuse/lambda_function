#!/usr/bin/python
import json
import re
import requests
from threading import Timer, Lock
from bs4 import BeautifulSoup

TELEGRAM_BOT = ""


def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            raise Exception('请求失败')
        return response.text
    except Exception as err:
        print(err)
        raise err


def get_json(html):
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find_all('script')
    for content in script:
        if 'window.__APOLLO_STATE__' in str(content):
            content = content.text
            pattern = r"window.__APOLLO_STATE__ = (.+);"
            json_data = re.findall(pattern, content)[0]
            return json_data
    return None


def jsonfy(javascript):
    try:
        json_data = json.loads(javascript)
        return json_data
    except Exception as err:
        print(err)
        raise err


def prepare_weather_message():
    # get weather today
    weather_api = "https://weather.gc.ca/api/app/en/Location/MB-38?type=city"
    weather_json = jsonfy(get_html(weather_api))[0]
    alert = weather_json["alert"]
    time_stamp = weather_json["observation"]["timeStampText"]
    temperature = weather_json["observation"]["temperature"]["metric"]
    pressure = weather_json["observation"]["pressure"]["metric"]
    visibility = weather_json["observation"]["visibility"]["metric"]
    wind_direction = weather_json["observation"]["windDirection"]
    wind_speed = weather_json["observation"]["windSpeed"]["metric"]
    low_hi = weather_json["dailyFcst"]["regionalNormals"]["metric"]["text"]
    today_summary = weather_json["dailyFcst"]["daily"][0]["text"]
    tomorrow_summary = weather_json["dailyFcst"]["daily"][1]["text"]
    sunset = weather_json["riseSet"]["set"]["time"]
    sunrise = weather_json["riseSet"]["rise"]["time"]
    weather_message = ""
    if str(alert) != "{}":
        weather_message = weather_message + str(alert)
    weather_message = "Weather at {} is: {}°C, {}kPa, {}km visibility, wind {} {}km/h  " \
                      "temperature between {} sunset {} sunrise {}.  \n" \
                      "Today: {} \nTomorrow: {}".format(time_stamp, temperature, pressure, visibility,
                                                        wind_direction, wind_speed,
                                                        low_hi, sunset, sunrise,
                                                        today_summary, tomorrow_summary)
    return weather_message


def prepare_gas_message():
    gas_api = "https://www.gasbuddy.com/station/125491"
    data = jsonfy(get_json(get_html(gas_api)))
    station_125491 = data["Station:125491"]["prices"]
    regular_gas = (station_125491[0]["credit"]["price"])
    premium_gas = (station_125491[1]["credit"]["price"])
    updated_time = (station_125491[1]["credit"]["postedTime"])
    station_66606 = data["Station:66606"]["prices"]
    esso_gas = (station_66606[0]["credit"]["price"])
    gas_message = "costco regular_gas price is {0} " \
                  "costco premium_gas price is {1} " \
                  "updated at {2}. " \
                  "neer by ESSo regular gas price is {3}".format(regular_gas, premium_gas, updated_time, esso_gas)
    return gas_message


def send_telegram(message):
    # # # get
    # # base_url = "https://api.telegram.org/bot{}/getUpdates".format(TELEGRAM_BOT)
    # # # send
    global TELEGRAM_BOT
    base_url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_BOT)
    parameters = {
        "chat_id": "-1001816097693",
        "text": message
    }
    resp = requests.get(base_url, data=parameters)
    return resp.text


def do_jobs():
    weather_message = prepare_weather_message()
    print(weather_message)
    send_telegram(weather_message)
    gas_message = prepare_gas_message()
    print(gas_message)
    send_telegram(gas_message)


def lambda_handler(event, context):
    do_jobs()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if __name__ == '__main__':
    lambda_handler(None, None)
