FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc g++ make && \
    apt-get clean

RUN pip install poetry
RUN pip install peewee==3.17.5

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

COPY ./app/data/initial/insert_basic_data.py /app/task.py

CMD ["python", "task.py"]
