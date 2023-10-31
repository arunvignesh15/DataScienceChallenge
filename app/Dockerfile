FROM python:3.8

WORKDIR /app/

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get update && apt-get -y install tesseract-ocr 

RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 main:app
