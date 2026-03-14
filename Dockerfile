FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv sync --no-dev

COPY . .

CMD ["uv", "run", "main.py"]