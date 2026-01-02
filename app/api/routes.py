from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.storage.s3 import generate_s3_presigned_url

from app.queue.sqs import enqueue_job


import uuid
import logging

logger = logging.getLogger("api.routes")

# Configuration
ALLOWED_EXT = {"png", "jpg", "jpeg"}

# API Router
router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse({"message": "Hello from FastAPI"})


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        # Validate extension
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXT:
            raise HTTPException(
                status_code=400,
                detail=f"Only {', '.join(ALLOWED_EXT)} files are allowed",
            )

        # Generate unique job ID and S3 key
        job_id = str(uuid.uuid4())
        s3_key = f"uploads/{job_id}/{file.filename}"

        try:
            # Generate presigned URL
            upload_url = generate_s3_presigned_url(
                key=s3_key,
                content_type=file.content_type,
            )
        except Exception as e:
            logger.error(
                f"Error generating presigned URL: {str(e)} {s3_key} {file.content_type}"
            )
            raise HTTPException(status_code=500, detail="Could not generate upload URL")

        return {
            "upload_url": upload_url,
            "s3_key": s3_key,
            "job_id": job_id,
            "message": "Upload URL generated successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/submit")
async def submit_file(job_id: str, s3_key: str):
    # TODO: validate if file exists in S3
    # TODO: add in db for later tracking

    # Enqueue job immediately
    enqueue_job(job_id, s3_key)

    return {"job_id": job_id, "message": "Job submitted successfully"}


@router.get("/health")
async def health():
    return {"status": "Service alive!"}
