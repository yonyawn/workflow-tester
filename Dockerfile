# Stage 1: Run tests
FROM python:3.14-slim AS test
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml .
RUN uv sync --group dev
COPY . .
RUN uv run pytest

# Stage 2: Production app
# COPY --from=test creates a hard dependency — if tests fail, this stage never runs
FROM python:3.14-slim AS final
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY --from=test /app/pyproject.toml .
RUN uv sync --no-dev
COPY calculator.py main.py ./
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]