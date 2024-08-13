# API Keys and Tokens
API_KEY = 'e88b7076916a44e2bc680017240208'
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"
TELEGRAM_BOT_TOKEN = '7401188794:AAFaOOHz17gBqI-rfNH03vC4_oYV3_Mwh6Y'
EVENTS_API_KEY = '8a84817183msh01777bf1abb81dap1ec141jsn43bd0b538d8d'
EVENTS_API_HOST = 'concerts-artists-events-tracker.p.rapidapi.com'

# Database Configuration
DB_CONFIG = {
    'user': 'root',
    'password': 'rootpassword',
    'host': 'mariadb',
    'database': 'exampledb',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci' 
}

# MinIO Configuration
MINIO_CONFIG = {
    'endpoint': 'minio:9000',
    'access_key': 'minioadmin',
    'secret_key': 'minioadmin',
    'secure': False
}

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = ['kafka:9092']

# Bot Configuration
DAYS_ADD = 13