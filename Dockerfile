FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/
COPY assignment/start.sh /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./assignment /app/
