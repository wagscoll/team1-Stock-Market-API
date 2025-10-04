# Use lightweight Python base image
FROM python:3.12-alpine

# Set environment variables for Poetry and AWS usage
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=/app

ENV PATH="${POETRY_HOME}/bin:$PATH"

# Install system dependencies
RUN apk add --no-cache curl build-base

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install project dependencies (excluding the project itself)
RUN poetry install --no-root

# Optional: install AWS SDK
RUN poetry add boto3

# Expose port 80 for incoming HTTP traffic
EXPOSE 80

# Run the Quart app on port 80
CMD ["poetry", "run", "python", "-m", "api.server"]
