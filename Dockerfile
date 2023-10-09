# renovate: datasource=docker depName=python versioning=docker
ARG PYTHON_VERSION=3.11-slim-bookworm

FROM python:${PYTHON_VERSION}

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY src/ src/
COPY requirements.txt setup.py ./

RUN apt update &&\
    apt install -y gcc &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apt purge -y gcc &&\
    apt autoremove -y &&\
    apt clean &&\
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "src/td4a-server" ]
