from django.shortcuts import render
import requests

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = "f93d8d73d5e8f6363de83ddc183c8346"
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def home(request):
    # Initialize all variables with default values
    weather = None
    weather_description = None
    city = request.GET.get('city')
    country = None
    wind_speed = None
    pressure = None
    humidity = None
    temperature = None
    icon_url = 'https://openweathermap.org/img/wn/10d@2x.png'  # default icon

    if city:
        weather_data_result = get_weather(city)
        if weather_data_result is not None:
            try:
                icon_id = weather_data_result['weather'][0]['icon']
                icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
                
                # Extracting Details
                weather = weather_data_result['weather'][0]['main']
                weather_description = weather_data_result['weather'][0]['description']
                city = weather_data_result['name']
                country = weather_data_result['sys']['country']
                wind_speed = weather_data_result['wind']['speed']
                pressure = weather_data_result['main']['pressure']
                humidity = weather_data_result['main']['humidity']
                temperature = weather_data_result['main']['temp']
            except KeyError as e:
                # Handle any missing data in the API response
                print(f"Error processing weather data: {e}")

    # Single return statement with context
    context = {
        'icon_url': icon_url,
        'weather': weather,
        'weather_description': weather_description,
        'city': city,
        'country': country,
        'wind_speed': wind_speed,
        'pressure': pressure,
        'humidity': humidity,
        'temperature': temperature,
    }
    
    return render(request, 'index.html', context)