#!/bin/bash

echo "Activating Python virtual environment..."
source /opt/api/.venv/bin/activate

echo "Running alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload