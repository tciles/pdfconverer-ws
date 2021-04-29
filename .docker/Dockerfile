FROM debian:buster-slim

WORKDIR /

RUN apt-get -y update

RUN apt-get -y install --no-install-recommends --no-install-suggests \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    python3-wheel \
    supervisor \
    poppler-utils

RUN python3 -m pip install \
    flask \
    flask-cors \
    gunicorn \
    flasgger \
    rq \
    redis

COPY application/queue.conf /etc/supervisord.conf

# Server
WORKDIR /www
COPY application/*.py /www/
COPY application/templates /www/templates

