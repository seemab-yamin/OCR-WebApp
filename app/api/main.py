from fastapi import FastAPI
import uvicorn
from mangum import Mangum
import os
import logging
import sys

from app.api import routes  # import your routes module

# Lambda has a read-only filesystem; use stdout (→ CloudWatch) instead of file
if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
else:
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/api.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

logger = logging.getLogger("api")

ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app = FastAPI(
    title="OCR Web Application",
    description="OCR Web Application allows extracting text via OCR from images.",
    version="1.0.0",
)

# Include routes
app.include_router(routes.router)

# Lambda handler (used when deployed to AWS)
handler = Mangum(app, lifespan="off")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
