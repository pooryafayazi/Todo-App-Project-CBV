# Dockerfile
FROM python:3.10-slim-buster

LABEL maintainer="poorya189@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .


RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install python-decouple

COPY ./core .

# RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]