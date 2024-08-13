from minio import Minio
from minio.error import S3Error
from config import MINIO_CONFIG

def setup_minio_bucket(bucket_name):
    minio_client = Minio(**MINIO_CONFIG)

    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully")
        else:
            print(f"Bucket '{bucket_name}' already exists")
    except S3Error as err:
        print(f"Error occurred: {err}")

if __name__ == "__main__":
    bucket_name = "bot-messages-bucket"
    setup_minio_bucket(bucket_name)