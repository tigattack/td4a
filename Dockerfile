ARG PYTHON_VER='3.8'

FROM python:${PYTHON_VER}-slim-bookworm

ARG PYTHON_VER
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY src/ src/
COPY requirements.txt setup.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "src/td4a-server" ]
