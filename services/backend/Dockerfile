FROM python:3.10.11-bullseye

WORKDIR /src
COPY pyproject.toml /

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["poetry", "run", "python3", "main.py"]