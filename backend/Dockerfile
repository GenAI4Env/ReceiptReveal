FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
ENV POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app
CMD ["poetry", "run", "start"]
