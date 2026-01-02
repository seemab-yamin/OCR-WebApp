from fastapi import FastAPI
import uvicorn
import os

from app.api import routes  # import your routes module

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

import logging

logging.basicConfig(filename="logs/api.log", level=logging.INFO)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
