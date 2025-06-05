FROM python:3.13-slim

WORKDIR /usr/src/app

# set environment variables - has advantages for python in docker cointainer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt install -y wget \
    && apt install -y unzip \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://github.com/fkrenn12/API-MQTT-Gateway/archive/master.zip \
    && unzip master.zip \
    && rm -rf master.zip \
    && cp ./API-MQTT-Gateway-master/api/* . \
    && rm -rf ./API-MQTT-Gateway-master \
    && rm -rf Dockerfile*

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

