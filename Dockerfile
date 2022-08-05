FROM python:3.10-slim

WORKDIR /app

COPY app/ .

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install --no-cache-dir poetry

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python3", "main.py"]