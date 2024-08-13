from kafka import KafkaConsumer
import json
from minio import Minio
import io
from config import MINIO_CONFIG, KAFKA_BOOTSTRAP_SERVERS

minio_client = Minio(**MINIO_CONFIG)

consumer = KafkaConsumer(
    'minio-messages',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def write_to_minio(message_data):
    bucket_name = "bot-messages-bucket"
    object_name = f"message_{message_data['chat_id']}_{message_data['timestamp']}.json"
    
    try:
        json_data = json.dumps(message_data).encode('utf-8')
        minio_client.put_object(
            bucket_name, object_name, io.BytesIO(json_data), len(json_data),
            content_type="application/json"
        )
        print(f"Message saved to MinIO: {object_name}")
    except Exception as err:
        print(f"Failed to save message to MinIO: {err}")

for message in consumer:
    write_to_minio(message.value)