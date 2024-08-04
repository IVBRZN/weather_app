from django.http import HttpResponse
from django.shortcuts import render
from geopy.geocoders import Nominatim #Подключаем библиотеку
from openmeteopy import OpenMeteo
from openmeteopy.hourly import HourlyForecast
from openmeteopy.daily import DailyForecast
from openmeteopy.options import ForecastOptions
from .models import City
import json
from .forms import CityForm

def index(request):

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    geolocator = Nominatim(user_agent="admin") 
    
    form = CityForm()

    cities = City.objects.all()

    all_cities = []
    
    for city in cities:
         #Получаем интересующий нас адрес
        location = geolocator.geocode(city) #Создаем переменную, которая состоит из нужного нам адреса
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

        zipped = zip(py_obj_temp_max['daily']['time'], py_obj_temp_min['daily']['temperature_2m_min'], py_obj_temp_max['daily']['temperature_2m_max'])
        city_info = {
            'city': city.name,
            'zip': list(zipped)
            }

        all_cities.append(city_info)
    
    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)