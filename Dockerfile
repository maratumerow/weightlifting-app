FROM python:3.12-slim

WORKDIR /weightlifting-app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /weightlifting-app/
COPY app /weightlifting-app/app
COPY alembic /weightlifting-app/alembic
COPY alembic.ini /weightlifting-app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root

ENV PORT=8000

EXPOSE $PORT

CMD ["sh", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port ${PORT} && poetry run alembic revision --autogenerate -m 'Initial migration' && poetry run alembic upgrade head"]  