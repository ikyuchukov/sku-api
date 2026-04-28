FROM python:3.13-slim
LABEL authors="ilian"

# Get UV directly from image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app
COPY . /app

RUN useradd --create-home api && chown -R api:api /app
USER api
# Install libraries and ensure versions are locked
# --no-cache to avoid image size increase
RUN uv sync --locked --no-cache

CMD uv run alembic upgrade head && /app/.venv/bin/fastapi run app/main.py --port 80 --host 0.0.0.0
