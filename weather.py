import requests
import json

current_weather = None

weather_table = [[200, 201, 202, 210, 211, 212, 221, 230, 231, 232],
                 [300, 301, 302, 310, 311, 312, 313, 314, 321],
                 [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
                 [600, 601, 602, 620, 621, 622],
                 [611, 612, 613, 615, 616],
                 [701, 711, 721, 731, 741, 751, 761, 762],
                 [771, 781],
                 [800],
                 [801, 802, 803, 804]]
weather_name = ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'SnowRain',
                'Fog', 'Wind', 'Clear', 'Clouds']

city_name = "Shanghai"
api_key = "xxx"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}


def get_weather():
    """
    Get current weather.
    """
    global current_weather
    try:
        response = requests.get(url, proxies=proxy)
    except:
        current_weather = None
        return None
    data = json.loads(response.text)
    description_id = data["weather"][0]["id"]
    for i in range(len(weather_name)):
        if description_id in weather_table[i]:
            current_weather = weather_name[i]
            return weather_name[i]
    current_weather = None
    return None


if __name__ == '__main__':
    print(get_weather())


