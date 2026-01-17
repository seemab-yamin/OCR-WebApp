import time
import os
from app.db.dynamodb import dynamodb

TABLE_NAME = os.getenv("OCR_JOBS_TABLE")
table = dynamodb.Table(TABLE_NAME)

# Time to live for job records in seconds
TTL_SECONDS = 24 * 60 * 60  # 24 hours

def create_job(job_id: str, input_s3_key: str):
    now = int(time.time())
    table.put_item(
        Item={
            "job_id": job_id,
            "status": "QUEUED",
            "input_s3_key": input_s3_key,
            "created_at": now,
            "expires_at": now + TTL_SECONDS,
        }
    )

def update_job(job_id: str, **fields):
    update_expr = []
    values = {}
    for k, v in fields.items():
        update_expr.append(f"{k} = :{k}")
        values[f":{k}"] = v

    table.update_item(
        Key={"job_id": job_id},
        UpdateExpression="SET " + ", ".join(update_expr),
        ExpressionAttributeValues=values,
    )

def get_job(job_id: str):
    resp = table.get_item(Key={"job_id": job_id})
    return resp.get("Item")
