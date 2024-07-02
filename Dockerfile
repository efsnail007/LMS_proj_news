FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip && pip --no-cache-dir install poetry

WORKDIR /app

COPY src /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false
RUN poetry install