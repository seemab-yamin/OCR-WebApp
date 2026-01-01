# OCR WebApp

## Project Overview
FastAPI-based web application for Optical Character Recognition (OCR) with REST API endpoints.

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
docker build -t ocr-webapp .

docker run -p 8000:8000 ocr-webapp

docker run -it -p 8000:8000 -v "${PWD}:/app" ocr-webapp /bin/bash

jupyter notebook \
  --port 8000 \
  --no-browser \
  --ip=0.0.0.0 \
  --allow-root \
  --NotebookApp.token='' \
  --NotebookApp.password=''

docker start -ai 6cf5b9ef1db7bb3db59f85c5fe8da3af00883cccf30244f4c764720b947c3b6b

docker cp "C:\Users\pc\Documents\SEEMAB\ocr-webapp\sample.png" "6cf5b9ef1db7bb3db59f85c5fe8da3af00883cccf30244f4c764720b947c3b6b:/app"