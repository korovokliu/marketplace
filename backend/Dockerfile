FROM python:3.9-alpine

ENV PYTHONUNBUFFERED = 1
ENV DONTWRITEBYTECODE = 1

COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./requirements.txt /tmp/requirements.txt
COPY ./test_django_deploy /test_django_deploy

WORKDIR /test_django_deploy
EXPOSE 8000

# по умолчанию мы не запущены в development-режиме, но если запущены в нем, то
# устанавливать так же будут необходимые библиотеки (flake8) из requirements.dev.txt
ARG DEV=false

RUN python -m venv .venv && \
    /.venv/bin/pip install --upgrade pip && \
    /.venv/bin/pip install -r /tmp/requirements.txt && \
    if [$DEV = "true"]; \
      then /.venv/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    useradd django

ENV PATH="/.venv/bin:$PATH"

USER django