FROM python:3.10-slim AS base

RUN apt-get update \
    && apt-get install -y gcc libev4 libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend/ws

FROM base AS dev_req

COPY pyproject.toml poetry.lock /app/backend/ws/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/ws/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM base AS prod_req

COPY pyproject.toml poetry.lock /app/backend/ws/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/ws/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM base AS dev

COPY --from=dev_req /app/backend/ws/requirements.txt /app/backend/ws/

RUN pip install -r requirements.txt

COPY ./ /app/backend/ws/
RUN chmod +x /app/backend/ws/entrypoint.sh

FROM base AS prod

COPY --from=prod_req /app/backend/ws/requirements.txt /app/backend/ws/

RUN pip install -r requirements.txt

COPY ./ /app/backend/ws/
RUN chmod +x /app/backend/ws/entrypoint.sh