from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import logging
from config import KAFKA_BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic, message):
    future = producer.send(topic, message)
    try:
        record_metadata = future.get(timeout=10)
        logger.debug(f"Message sent to Kafka topic {topic}: {record_metadata.topic}")
    except KafkaError as e:
        logger.error(f"Failed to send message to Kafka: {e}")