FROM ghcr.io/astral-sh/uv:python3.9-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY *.py ./
ENTRYPOINT ["uv", "run", "python", "trello_service.py"]
