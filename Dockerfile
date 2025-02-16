# Use Python 3.9 (matches pyproject.toml)
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/opt/poetry/bin:$PATH"

# Set the working directory
WORKDIR /code

# Install system dependencies
RUN apk add --no-cache bash curl gcc musl-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

# Verify Poetry installation
RUN poetry --version

# Copy Poetry config files before installing dependencies (for caching)
COPY pyproject.toml poetry.lock /code/

# Install dependencies
RUN poetry install --no-root --only main

# Copy the rest of the application
COPY . /code/

# Expose the FastAPI port
EXPOSE 8000

# Make script executable
RUN chmod +x ./serve.sh

