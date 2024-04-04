FROM python:3.10.12-slim-buster AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

RUN apt-get update \
    && apt-get install -y gcc libev4 libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend


FROM base AS dev_req

COPY pyproject.toml poetry.lock /app/backend/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


FROM base AS prod_req

COPY pyproject.toml poetry.lock /app/backend/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


FROM base AS dev

COPY --from=dev_req /app/backend/requirements.txt /app/backend/

RUN pip install -r requirements.txt

COPY ./ /app/backend/


FROM base AS prod

COPY --from=prod_req /usr/src/app/requirements.txt /app/backend/

RUN pip install -r requirements.txt

COPY ./ /app/backend/
