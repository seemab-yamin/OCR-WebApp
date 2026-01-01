from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
import uvicorn
import io
from PIL import Image

import logging

logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app = FastAPI(
    title="OCR Web Application",
    description="OCR Web Application allows extracting text via OCR from images.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return JSONResponse({"message": "Hello from FastAPI"})


@app.post("/ocr/")
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

        # Validate file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")

        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        # Validate image format
        try:
            with Image.open(io.BytesIO(contents)) as image:
                # Verify it's a valid image
                image.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Process OCR
        with Image.open(io.BytesIO(contents)) as image:
            text = pytesseract.image_to_string(image).strip()

            if not text:
                logger.warning(f"No text extracted from {file.filename}")
                return {
                    "filename": file.filename,
                    "extracted_text": "",
                    "warning": "No text found",
                }

            return {"filename": file.filename, "extracted_text": text}

    except HTTPException:
        raise
    except pytesseract.TesseractNotFoundError:
        logger.error("Tesseract not installed")
        raise HTTPException(status_code=500, detail="OCR engine not configured")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health():
    return {"status": "Service alive!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
