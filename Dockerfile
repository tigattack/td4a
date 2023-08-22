# renovate: datasource=docker depName=python versioning=docker
ARG PYTHON_VERSION=3.8-slim-bookworm

FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY src/ src/
COPY requirements.txt setup.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "src/td4a-server" ]
