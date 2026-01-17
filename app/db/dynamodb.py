import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)