from PIL import Image

import requests
API_key = '0e9941e74c1774e755691c8b7dee96d1'

def get_weather_data(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 404:
        return None
    #parse response JSON
    data = response.json()
    icon_id = data['weather'][0]['icon']
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    city = data['name']
    country = data['sys']['country']

    #get icon URL and return all the weather information
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    image = Image.open(requests.get(icon_url, stream=True).raw)
    return city, temperature, description, country, icon_url, image


