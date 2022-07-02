FROM python:3.9-alpine

WORKDIR /app

COPY ./src /app
COPY ./.env /app/.env
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt