FROM python:3.12-alpine

WORKDIR backend

COPY app /app
COPY poetry.lock pyproject.toml /

ENV PATH="${PATH}:./poetry/bin"

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --only main --no-interaction

CMD ["bash", "-c", "uvicorn app.main:app"]
