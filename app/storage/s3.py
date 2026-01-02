"""
S3 helper functions for uploading and downloading files to/from AWS S3
"""

import os
import boto3

# AWS S3 Configuration
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
s3_client = boto3.client("s3", region_name=AWS_REGION)


def generate_s3_presigned_url(key: str, content_type: str, expires_in=300):
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=expires_in,
    )


def upload_s3_file(file_bytes: bytes, key: str):
    s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=file_bytes)


def download_s3_file(key: str):
    response = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
    return response["Body"].read()
