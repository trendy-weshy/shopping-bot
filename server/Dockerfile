
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

ENV HOST 0.0.0.0

COPY . /var/www/

WORKDIR /var/www/

RUN pip install -r requirements.txt --no-cache-dir --user

EXPOSE 5000 8000


