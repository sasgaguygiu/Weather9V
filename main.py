import weather_api

res = weather_api.get_periods_weather(52.52, 13.41, [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "precipitation_probability",
    "precipitation",
    "weather_code",
    "pressure_msl",
    "visibility",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m"
])
print(res)