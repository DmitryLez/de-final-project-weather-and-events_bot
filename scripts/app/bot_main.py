import logging
import datetime
import telebot
from config import TELEGRAM_BOT_TOKEN, DAYS_ADD
from weather_api import weather_api
from events_api import events_api
from kafka_producer import send_to_kafka
from top_cities import df_cities

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Define the maximum date range
max_date_range = datetime.datetime.now() + datetime.timedelta(days=DAYS_ADD)

def log_message(chat_id, user_id, message_text):
    message_data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "message_text": message_text,
        "timestamp": datetime.datetime.now().isoformat()
    }
    send_to_kafka("bot-messages", message_data)
    send_to_kafka("mariadb-messages", message_data)
    send_to_kafka("minio-messages", message_data)

def send_and_log_message(chat_id, text, user_id=None):
    bot.send_message(chat_id, text)
    log_message(chat_id, user_id, text)

def send_long_message(chat_id, text, user_id=None):
    max_length = 4096  # Telegram's maximum message length
    for i in range(0, len(text), max_length):
        chunk = text[i:i+max_length]
        send_and_log_message(chat_id, chunk, user_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    resp = f'''Hi! I'm Weather&Events Bot
I will help you to find the weather forecast and cool events for your desired location and date range!
Please provide the start date, end date, and location in the following format:
YYYY-MM-DD YYYY-MM-DD Location

Example:
2024-07-01 2024-07-10 London

Note:
1. The end date cannot be more than {DAYS_ADD} days from today ({max_date_range.strftime('%Y-%m-%d')}).
2. Choose one city from the following list.
'''
    logger.debug(f"Sending welcome message to chat ID: {message.chat.id}")
    send_and_log_message(message.chat.id, resp, message.from_user.id)

    cities_list = [f"{row['rank']}: {row['city']}, {row['country']}" for _, row in df_cities.iterrows()]
    cities_message = "Here are some popular cities you can choose from:\n" + "\n".join(cities_list)
    send_and_log_message(message.chat.id, cities_message, message.from_user.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_input = message.text.split(maxsplit=3)
        start_date = user_input[0]
        end_date = user_input[1]
        location = user_input[2]
        additional_info = user_input[3] if len(user_input) > 3 else ''

        if location.lower() not in df_cities['city'].str.lower().values:
            send_and_log_message(message.chat.id, f"'{location}' not in popular cities list. \nPlease choose a city from the list.", message.from_user.id)
            return

        start_date_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if end_date_dt > max_date_range:
            send_and_log_message(message.chat.id, f'The end date cannot be more than {DAYS_ADD} days from today. Please enter a valid date range.', message.from_user.id)
            return

        forecast = weather_api(location, start_date_dt, end_date_dt)

        if not forecast:
            send_and_log_message(message.chat.id, f'Could not fetch weather data for {location}. Please check the location and try again.', message.from_user.id)
            return

        response_message = f"Weather forecast for {location}:\n"
        for day in forecast:
            response_message += f"{day['date']}: Min Temp: {day['min_temp']}°C, Max Temp: {day['max_temp']}°C, {day['text']}\n"

        if additional_info:
            response_message += f"Additional Information: {additional_info}\n"

        send_long_message(message.chat.id, response_message, message.from_user.id)

        logger.debug(f"Calling events_api for {location} from {start_date_dt} to {end_date_dt}")
        events = events_api(location, start_date_dt, end_date_dt)
        
        logger.debug(f"Events API returned: {events}")

        if not events:
            send_and_log_message(message.chat.id, f'No events found for {location} during this period.', message.from_user.id)
            return

        events_message = f"Events in {location} from {start_date} to {end_date}:\n"
        for event in events:
            event_details = f"{event['title']}\nDate: {event['date']}\nTime: {event['time']}\nDescription: {event['description']}\nLocation: {event['location']}\n\n"
            if len(events_message) + len(event_details) > 4000:
                send_long_message(message.chat.id, events_message, message.from_user.id)
                events_message = f"More events in {location}:\n"
            events_message += event_details

        if events_message:
            send_long_message(message.chat.id, events_message, message.from_user.id)

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        error_message = f"An error occurred while processing your request: {str(e)}. Please try again.\n"
        error_message += f"Debug info: message={message.text}, error_type={type(e).__name__}"
        send_and_log_message(message.chat.id, error_message, message.from_user.id)

if __name__ == "__main__":
    logger.debug("Starting bot polling...")
    bot.polling()
    logger.debug("Bot polling started.")