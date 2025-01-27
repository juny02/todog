FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

WORKDIR /opt/api

COPY . /opt/api

RUN uv sync --frozen --no-cache

CMD ["/opt/api/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]