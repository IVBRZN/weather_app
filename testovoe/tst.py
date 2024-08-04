from geopy.geocoders import Nominatim #Подключаем библиотеку
from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions
import json


geolocator = Nominatim(user_agent="Ivan") #Указываем название приложения (так нужно, да)
adress = str(input('Введите адрес: \n')) #Получаем интересующий нас адрес
location = geolocator.geocode(adress) #Создаем переменную, которая состоит из нужного нам адреса
lat = location.latitude

lon = location.longitude

hourly_max = HourlyForecast()
daily_max = DailyForecast()

hourly_min = HourlyForecast()
daily_min = DailyForecast()

options = ForecastOptions(lat, lon)

mem_temp_max = OpenMeteo(options, hourly_max.temperature_2m(), daily_max.temperature_2m_max())
mem_temp_min = OpenMeteo(options, hourly_min.temperature_2m(), daily_min.temperature_2m_min())

# Download data
meteo_max = mem_temp_max.get_json_str()
meteo_min = mem_temp_min.get_json_str()

py_obj_temp_max = json.loads(meteo_max)
py_obj_temp_min = json.loads(meteo_min)

city_info = {
    'time': py_obj_temp_max['daily']['time'],
    'temperature_max': py_obj_temp_max['daily']['temperature_2m_max'],
    'temperature_min': py_obj_temp_min['daily']['temperature_2m_min']
}

print(city_info["temperature_max"]["daily"]['temperature_2m_max'])