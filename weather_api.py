import requests

url = "https://api.open-meteo.com/v1/forecast"


def get_daily_weather(latitude: float, longitude: float, parameters: [str]):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": parameters,
        "timezone": "Europe/Moscow",
        "forecast_days": 1
    }
    response = requests.get(url, params).json()['daily']
    result = {}
    for parameter in parameters:
        result.update({parameter: response[parameter][0]})
        if parameter in ['sunrise', 'sunset']:
            result[parameter] = result[parameter].split('T')[1]

    return result


def get_hourly_weather(latitude: float, longitude: float, parameters: [str]):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": parameters,
        "timezone": "Europe/Moscow",
        "forecast_days": 1
    }
    response = requests.get(url, params).json()['hourly']
    result = {}
    for parameter in parameters:
        result.update({parameter: response[parameter]})

    return response


avg = ['temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'visibility', 'wind_speed_10m',
       'wind_direction_10m']
maxx = ['precipitation_probability', 'weather_code', 'wind_gusts_10m']
summa = ['precipitation']


def get_period_parameter(parameter, a, begin, end):
    res = a[begin]
    for i in range(begin - 1, end):
        if parameter in maxx:
            res = max(res, a[i])
        else:
            res += a[i]
    if parameter in avg:
        res /= (end - begin)
    return res


def get_period(weather, begin, end):
    result = {}
    for parameter in weather:
        if parameter == 'time':
            continue
        result.update({parameter: get_period_parameter(parameter, weather[parameter], begin, end)})
    return result


def get_periods_weather(latitude: float, longitude: float, parameters: [str]):
    weather = get_hourly_weather(latitude, longitude, parameters)

    result = {
        'night': get_period(weather, 0, 6),
        'morning': get_period(weather, 6, 12),
        'day': get_period(weather, 12, 18),
        'evening': get_period(weather, 18, 24),
    }

    return result
