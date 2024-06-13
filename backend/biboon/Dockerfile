FROM python:3.12-slim AS base

RUN apt-get update \
    && apt-get install -y gcc libev4 libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend/biboon

ARG BIBOON_DEBUG
ARG BIBOON_RABBITMQ_USER
ARG BIBOON_RABBITMQ_PASS
ARG BIBOON_RABBITMQ_HOST
ARG BIBOON_RABBITMQ_PORT
ARG BIBOON_RABBITMQ_VHOST
ARG BIBOON_MONGO_DB_NAME
ARG BIBOON_MONGO_COLLECTION
ARG BIBOON_MONGO_HOST
ARG BIBOON_MONGO_PORT

ENV DEBUG=${BIBOON_DEBUG}
ENV RABBITMQ_USER=${BIBOON_RABBITMQ_USER}
ENV RABBITMQ_PASS=${BIBOON_RABBITMQ_PASS}
ENV RABBITMQ_HOST=${BIBOON_RABBITMQ_HOST}
ENV RABBITMQ_PORT=${BIBOON_RABBITMQ_PORT}
ENV RABBITMQ_VHOST=${BIBOON_RABBITMQ_VHOST}
ENV MONGO_DB_NAME=${BIBOON_MONGO_DB_NAME}
ENV MONGO_COLLECTION=${BIBOON_MONGO_COLLECTION}
ENV MONGO_HOST=${BIBOON_MONGO_HOST}
ENV MONGO_PORT=${BIBOON_MONGO_PORT}


FROM base AS dev_req

COPY pyproject.toml poetry.lock /app/backend/biboon/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/biboon/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM base AS prod_req

COPY pyproject.toml poetry.lock /app/backend/biboon/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/biboon/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

FROM base AS dev

COPY --from=dev_req /app/backend/biboon/requirements.txt /app/backend/biboon/

RUN pip install -r requirements.txt

COPY ./ /app/backend/biboon/
RUN chmod +x /app/backend/biboon/entrypoint.sh

FROM base AS prod

COPY --from=prod_req /app/backend/biboon/requirements.txt /app/backend/biboon/

RUN pip install -r requirements.txt

COPY ./ /app/backend/biboon/
RUN chmod +x /app/backend/biboon/entrypoint.sh