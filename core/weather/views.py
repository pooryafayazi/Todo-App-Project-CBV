from django.shortcuts import render
import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from django.utils import timezone
import jdatetime
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


"""
class WeatherView(View):
    def get(self, request):
        city = request.GET.get('city', 'Tehran')
        cache_key = f'weather_{city}'

        # check cache first
        weather_data = cache.get(cache_key)
        if weather_data:
        #     sunrise_timestamp = weather_data['sys']['sunrise']
        #     sunset_timestamp = weather_data['sys']['sunset']            
        #     weather_data['sys']['sunrise'] = timezone.datetime.fromtimestamp(sunrise_timestamp, tz=timezone.utc)
        #     weather_data['sys']['sunset'] = timezone.datetime.fromtimestamp(sunset_timestamp, tz=timezone.utc)           
            
            return JsonResponse(weather_data)
            # return render(request, 'tasks/weather_test.html', {'weather_data': weather_data})

        api_key = '392eced748e3ae4a7274d46e517f926d'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # check response status
            
            weather_data = response.json()
            
            sunrise_timestamp = weather_data['sys']['sunrise']
            sunset_timestamp = weather_data['sys']['sunset']

            # تبدیل timestamp به datetime
            weather_data['sys']['sunrise'] = timezone.make_aware(datetime.fromtimestamp(sunrise_timestamp))
            weather_data['sys']['sunset'] = timezone.make_aware(datetime.fromtimestamp(sunset_timestamp))
            
            
            cache.set(cache_key, weather_data)  # save data in cache

            return JsonResponse(weather_data)
            # return render(request, 'tasks/weather_test.html', {'weather_data': weather_data})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
 """       
        
        

# @cache_page(1200)
class WeatherView(View):
    @method_decorator(cache_page(1200), name='get')
    def get(self, request):
        city = request.GET.get('city', 'Tehran')
        cache_key = f'weather_{city}'

        # check cache first
        weather_data = cache.get(cache_key)
        if weather_data:
            return JsonResponse(weather_data)

        api_key = '392eced748e3ae4a7274d46e517f926d'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            weather_data = response.json()
            
            sunrise_timestamp = weather_data['sys']['sunrise']
            sunset_timestamp = weather_data['sys']['sunset']

            weather_data['sys']['sunrise'] = timezone.make_aware(datetime.fromtimestamp(sunrise_timestamp))
            weather_data['sys']['sunset'] = timezone.make_aware(datetime.fromtimestamp(sunset_timestamp))
            
            # Convert to Jalali date
            self.convert_to_jalali(weather_data)

            # save data in cache
            cache.set(cache_key, weather_data)  

            return JsonResponse(weather_data)
            
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

    def convert_to_jalali(self, weather_data):
        for key in ['sunrise', 'sunset']:
            if key in weather_data['sys']:
                # Get the aware datetime object
                dt_utc = weather_data['sys'][key]
                # Convert to local time (Asia/Tehran)
                dt_local = timezone.localtime(dt_utc)
                # Convert to Jalali date
                jalali_date = jdatetime.datetime.fromgregorian(
                    year=dt_local.year,
                    month=dt_local.month,
                    day=dt_local.day,
                    hour=dt_local.hour,
                    minute=dt_local.minute,
                    second=dt_local.second
                )
                # Set the format as desired
                weather_data['sys'][key] = jalali_date.strftime('%Y-%m-%d %H:%M:%S')  
