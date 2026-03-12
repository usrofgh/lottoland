FROM python:3.14-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV PYTHONPATH=/app

WORKDIR /app
COPY ../pyproject.toml ../uv.lock ./
RUN pip install uv && uv sync && rm pyproject.toml uv.lock
COPY src ./
