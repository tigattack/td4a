# renovate: datasource=github-tags depName=python/cpython
ARG PYTHON_VERSION=v3.11.4

FROM python:${PYTHON_VERSION}-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY src/ src/
COPY requirements.txt setup.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "src/td4a-server" ]
