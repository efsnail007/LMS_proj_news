FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip && pip --no-cache-dir install poetry

COPY src /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.create false
RUN poetry install


