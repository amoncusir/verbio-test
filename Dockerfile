ARG PYTHON_VERSION=3.13
ARG PROJECT_VERSION=0.0.0-unknown
ARG PROJECT_NAME=unknown
ARG TINI_VERSION=v0.19.0

# Used at least the minimum version defined in .python-version file, allowing patch updates
FROM python:${PYTHON_VERSION} AS poetry

ENV PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3

# Catch the dependency layer to speedup the build
FROM poetry AS env_ready

WORKDIR /opt

COPY poetry.toml poetry.lock pyproject.toml /opt/

RUN poetry install --only main --no-interaction --no-ansi --no-root

FROM env_ready AS final

ARG PROJECT_VERSION
ENV PROJECT_VERSION=$PROJECT_VERSION

ARG PROJECT_NAME
ENV PROJECT_NAME=$PROJECT_NAME

COPY . /opt/

# Set defailt shutdown signal
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s \
  CMD curl -f http://localhost:8000/status/healthcheck || exit 1

# Delegated to the script the shell election
ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["api", "--host=0.0.0.0", "--port=8000"]
