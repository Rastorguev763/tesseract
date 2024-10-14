#!/bin/sh
echo "Run tesseract..."

gunicorn src.main:app --bind=0.0.0.0:5050  --workers 1 --worker-class uvicorn.workers.UvicornWorker