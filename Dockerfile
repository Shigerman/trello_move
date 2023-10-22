FROM python:3.9
WORKDIR /app
COPY * ./
RUN pip install poetry
RUN poetry install
ENTRYPOINT poetry run python trello_service.py
