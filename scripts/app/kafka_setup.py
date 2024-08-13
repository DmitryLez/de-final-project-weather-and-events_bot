from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from config import KAFKA_BOOTSTRAP_SERVERS

def setup_kafka_topics():
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id='bot-admin'
    )

    topic_list = [
        NewTopic(name="bot-messages", num_partitions=1, replication_factor=1),
        NewTopic(name="mariadb-messages", num_partitions=1, replication_factor=1),
        NewTopic(name="minio-messages", num_partitions=1, replication_factor=1)
    ]

    for topic in topic_list:
        try:
            admin_client.create_topics([topic])
            print(f"Topic '{topic.name}' created successfully")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic.name}' already exists")
        except Exception as e:
            print(f"Error creating topic '{topic.name}': {e}")

    admin_client.close()

if __name__ == "__main__":
    setup_kafka_topics()