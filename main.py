from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
import uvicorn
import io
from PIL import Image

ALLOWED_EXT = {"png", "jpg", "jpeg"}

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse({"message": "Hello from FastAPI"})

@app.post("/ocr/")
async def upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Only {', '.join(ALLOWED_EXT.upper())} files are allowed")

    contents = await file.read()  # <-- file bytes here
    # process file
    with Image.open(io.BytesIO(contents)) as image:
        text = pytesseract.image_to_string(image)
        return {"filename": file.filename, "extracted_text": text}


@app.get("/health")
async def health():
    return {"status": "Service alive!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
