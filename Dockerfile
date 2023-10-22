FROM python:3.9
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install
COPY *.py ./
ENTRYPOINT poetry run python trello_service.py
