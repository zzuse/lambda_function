#!/usr/bin/python
import json
import re
import requests
from bs4 import BeautifulSoup


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
    soup = BeautifulSoup(html, 'lxml')
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


def lambda_handler(event, context):

    # # get weather today
    gas_api = "https://www.gasbuddy.com/station/125491"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'}
    resp_gas = requests.get(gas_api, headers=headers)
    print(resp_gas.text)

    weather_api = "https://weather.gc.ca/api/app/en/Location/MB-38?type=city"
    resp_weather = requests.get(weather_api, headers=headers)
    print(resp_weather.text)

    data = jsonfy(get_json(get_html(gas_api)))["Station:125491"]["prices"]
    print(data[0]["credit"])
    print(data[1]["credit"])

    TELEGRAM_BOT = ""
    # # get
    base_url = "https://api.telegram.org/bot{}/getUpdates".format(TELEGRAM_BOT)
    # # send
    base_url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_BOT)
    #
    # parameters = {
    #     "chat_id": "-1001816097693",
    #     "text": "haha"
    # }
    #
    # resp = requests.get(base_url, data=parameters)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if __name__ == '__main__':
    lambda_handler(None, None)
