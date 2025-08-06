FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    git \
    curl \
    nano

RUN python3.10 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install \
    langchain \
    langchain-mcp-adapters \
    httpx \
    redis \
    influxdb-client \
    tabulate \
    duckduckgo-search

WORKDIR /app
EXPOSE 8089

ENTRYPOINT ["python3", "main.py"]
