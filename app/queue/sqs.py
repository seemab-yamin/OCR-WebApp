"""
SQS helper functions for sending and receiving messages to/from AWS SQS
"""

import boto3
import os
import json
import uuid

OCR_QUEUE_URL = os.getenv("OCR_QUEUE_URL")
AWS_REGION = os.getenv("AWS_REGION")

sqs_client = boto3.client("sqs", region_name=AWS_REGION)


def enqueue_job(job_id: str, s3_key: str):
    message_body = json.dumps({"job_id": job_id, "s3_key": s3_key})
    return sqs_client.send_message(
        QueueUrl=OCR_QUEUE_URL,
        MessageBody=message_body,
        MessageGroupId="ocr-jobs-group",
    MessageDeduplicationId=str(uuid.uuid4())
    )


def poll_job():
    response = sqs_client.receive_message(
        QueueUrl=OCR_QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    if not messages:
        return None
    msg = messages[0]
    receipt_handle = msg["ReceiptHandle"]
    body = json.loads(msg["Body"])
    return body, receipt_handle


def delete_job(receipt_handle: str):
    sqs_client.delete_message(QueueUrl=OCR_QUEUE_URL, ReceiptHandle=receipt_handle)
