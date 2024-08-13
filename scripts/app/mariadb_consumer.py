from kafka import KafkaConsumer
import json
import mysql.connector
from config import DB_CONFIG, KAFKA_BOOTSTRAP_SERVERS

consumer = KafkaConsumer(
    'mariadb-messages',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def insert_message(chat_id, user_id, message_text, timestamp):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO bot_messages (chat_id, user_id, message_text, sent_at)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (chat_id, user_id, message_text, timestamp))
        
        connection.commit()
        print(f"Message inserted into MariaDB: {chat_id}, {user_id}, {message_text[:50]}...")
    except mysql.connector.Error as error:
        print(f"Failed to insert message into MySQL table: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

for message in consumer:
    data = message.value
    insert_message(data['chat_id'], data['user_id'], data['message_text'], data['timestamp'])