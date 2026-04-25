FROM python:3.13-slim
LABEL authors="ilian"

# Get UV directly from image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app
COPY . /app

# Install libraries and ensure versions are locked
RUN uv sync --locked

ENTRYPOINT ["tail", "-f", "/dev/null"]