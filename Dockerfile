###############################################
# Base Image
###############################################
# Use an official Python runtime as a parent image
FROM python:3.9.5-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV WAIT_VERSION=2.7.2

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-root
COPY entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]
COPY . /app
WORKDIR /app

CMD daphne broma_config.asgi:application -b 0.0.0.0 -p $PORT



# This Dockerfile sets up a Python-based environment using poetry for dependency management.
# Base Image: Uses python:3.9.5-slim. Configures environment variables for Python and poetry,
# including disabling the pip cache and setting a default timeout for pip operations.
# A 'wait' script is added and made executable to synchronize the container startup in docker-compose.

# Builder Image: Extends the python-base. Installs necessary packages like curl and build-essential for building Python packages.
# Sets up the working directory at PYSETUP_PATH and copies over the poetry configuration files.
# Installs project dependencies via poetry without creating a virtual environment.
# Copies the application code to /app, runs Django migrations, and exposes port 8000 for web access.
