FROM python:3.12-slim

WORKDIR /weightlifting-app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /weightlifting-app/
COPY app /weightlifting-app/app
COPY alembic.ini /weightlifting-app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root

ENV PORT=8000

EXPOSE $PORT

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --reload"]