import requests
import logging
import re
from config import EVENTS_API_KEY, EVENTS_API_HOST

logger = logging.getLogger(__name__)

def events_api(location, start_date, end_date):
    querystring = {
        "name": location,
        "minDate": start_date.strftime('%Y-%m-%d'),
        "maxDate": end_date.strftime('%Y-%m-%d'),
        "page": "1"
    }
    headers = {
        "x-rapidapi-key": EVENTS_API_KEY,
        "x-rapidapi-host": EVENTS_API_HOST
    }

    logger.debug(f"Making events API request for {location} from {start_date} to {end_date}")
    response = requests.get("https://concerts-artists-events-tracker.p.rapidapi.com/location", headers=headers, params=querystring)
    logger.debug(f"Events API Response status code: {response.status_code}")
    
    if response.status_code != 200:
        logger.error(f"Events API request failed with status code {response.status_code}: {response.text}")
        return []

    data = response.json()
    logger.debug(f"Received events data: {data}")

    events_data = []
    if 'data' in data:
        for event in data['data']:
            event_date_time = event.get('startDate', 'Unknown date').replace('T', ' ')
            event_date_parts = event_date_time.split(' ')
            event_date = event_date_parts[0] if event_date_parts else 'Unknown date'
            event_time = event_date_parts[1].split('+')[0] if len(event_date_parts) > 1 else 'Unknown time'
            
            event_title = event.get('name', 'No title')
            event_description = event.get('description', 'No description').replace('T', ' ').split('+')[0]
            event_location = event.get('location', {})
            address = event_location.get('address', {})
            address_country = address.get('addressCountry', '')
            address_locality = address.get('addressLocality', '')
            street_address = address.get('streetAddress', 'No street address')
            event_address = f"{street_address}, {address_locality}, {address_country}"

            if re.search(location, address_country, re.IGNORECASE) or re.search(location, address_locality, re.IGNORECASE):
                events_data.append({
                    'date': event_date,
                    'time': event_time,
                    'title': event_title,
                    'description': event_description,
                    'location': event_address
                })
    else:
        logger.error(f"No events data available for location {location}")

    return events_data