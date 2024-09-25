FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc g++ make && \
    apt-get clean

RUN pip install poetry
RUN pip install  peewee==3.17.6

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
