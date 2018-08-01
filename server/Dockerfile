
FROM python:3.6

ENV PYTHONUNBUFFERED 1

ENV HOST 0.0.0.0

ENV MONGODB_URI=mongodb://localhost:27072/jumia_catalog-db

COPY . /voke/

WORKDIR /voke/

RUN pip install -r requirements.txt

EXPOSE 5000 8000


