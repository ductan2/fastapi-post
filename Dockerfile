
FROM python:3.12.3-slim
WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install poetry

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
