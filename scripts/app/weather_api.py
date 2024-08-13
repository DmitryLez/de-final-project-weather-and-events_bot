import requests
import logging
import datetime
from config import API_KEY, BASE_URL

logger = logging.getLogger(__name__)

def weather_api(location, start_date, end_date):
    forecast_data = []
    date_range = (end_date - start_date).days + 1

    for day in range(date_range):
        date = (start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        querystring = {
            "key": API_KEY,
            "q": location,
            "dt": date,
            "days": 1
        }

        logger.debug(f"Making API request for {location} on {date}")
        response = requests.get(BASE_URL, params=querystring)
        logger.debug(f"API Response status code: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            continue

        data = response.json()

        if 'forecast' in data and data['forecast']['forecastday']:
            day_forecast = data['forecast']['forecastday'][0]['day']
            forecast_data.append({
                'date': date,
                'min_temp': day_forecast['mintemp_c'],
                'max_temp': day_forecast['maxtemp_c'],
                'text': day_forecast['condition']['text']
            })
        else:
            logger.error(f"No forecast data available for {date}")

    return forecast_data