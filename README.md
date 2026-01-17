# OCR WebApp

## Project Overview
FastAPI-based web application for Optical Character Recognition (OCR) with REST API endpoints.

## Features:
- OCR: Extract Text from images

- Logging: For debugging and monitoring

- Health Check: An endpoint to check availability without performing full functionality

- Dockerized Solution provides Easy Scaling & Deployment

- FastAPI provides native Async request processing

- Validation and Error Handling

## Demo
[![OCR WebApp Demo](https://img.youtube.com/vi/qkMXNliMgt4/0.jpg)](https://youtu.be/qkMXNliMgt4)

## Project Structure
```
ocr-webapp/
├── .dockerignore
├── .git/
├── .gitignore
├── Blueprint.md
├── dockerfile
├── main.py
├── ocr-execution.ipynb
├── README.md
├── requirements.txt
```

### File Descriptions
- **main.py** - FastAPI application with OCR endpoints
- **requirements.txt** - Python dependencies
- **dockerfile** - Docker configuration for containerization
- **ocr-execution.ipynb** - Jupyter notebook for OCR testing and development
- **Blueprint.md** - Project blueprint and design documentation

## Docker Commands
docker build -f Dockerfile.api -t ocr-webapp-api .

docker run --env-file .env -p 8000:8000 ocr-webapp-api

docker run -it -p 8000:8000 -v "${PWD}:/app" ocr-webapp-api /bin/bash

jupyter notebook \
  --port 8000 \
  --no-browser \
  --ip=0.0.0.0 \
  --allow-root \
  --NotebookApp.token='' \
  --NotebookApp.password=''

docker start -ai 6cf5b9ef1db7bb3db59f85c5fe8da3af00883cccf30244f4c764720b947c3b6b

docker cp "sample.png" "6cf5b9ef1db7bb3db59f85c5fe8da3af00883cccf30244f4c764720b947c3b6b:/app"

## CURL Command To Upload Images on Presigned Url

PRESIGNED_URL=''


#### For PNG
curl -X PUT \
     -H "Content-Type: image/png" \
     --upload-file /Users/levi/Downloads/ocr-test-1.png \
     "$PRESIGNED_URL"


#### For JPEG (works for both .jpg and .jpeg extension)
curl -X PUT \
     -H "Content-Type: image/jpeg" \
     --upload-file /path/to/your/photo.jpg \
     "$PRESIGNED_URL"