#!/bin/sh
BUCKET_NAME=minio/app-minio-data-bucket
# Start MinIO
minio server /data --console-address ":9001" &

# Wait for MinIO to start
sleep 5

# Configure mc
mc alias set minio http://localhost:9000 minioadmin minioadmin

# Create a bucket
mc mb $BUCKET_NAME

# Set policy
mc policy set public $BUCKET_NAME

# Keep the container running
wait

