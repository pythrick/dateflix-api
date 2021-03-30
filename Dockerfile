FROM python:3.9.2-buster AS python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.1.5 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# `development` image is used during development / testing
FROM python-base as development
ENV DJANGO_ENV=development

# install poetry - respects $POETRY_VERSION
RUN python -m pip install poetry==$POETRY_VERSION

WORKDIR /pysetup
COPY pyproject.toml ./

# install runtime deps
RUN poetry install
WORKDIR /app

# `production` image used for runtime
FROM python-base as production
ENV DJANGO_ENV=production


# install poetry - respects $POETRY_VERSION
RUN python -m pip install poetry==$POETRY_VERSION

WORKDIR /pysetup
COPY poetry.lock pyproject.toml /app/

# install runtime deps
RUN poetry install --no-dev

WORKDIR /app
COPY . /app/
