# python_realtime_pricing

requirements:
python3.10

how to use:

1. pip install poetry
2. poetry install
3. poetry run python3 main.py
4. open http://127.0.0.1/
5. profit

how to use in docker:

1. docker build --pull --rm -f "Dockerfile" -t pricing:latest "."
2. docker run pricing:latest
3. profit