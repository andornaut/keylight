ARG PYTHON_VERSION=3.12
FROM node:24.22.2 AS markdown
WORKDIR /opt/markdown
COPY tests/container/package.json tests/container/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund

FROM python:${PYTHON_VERSION}
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    POETRY_VIRTUALENVS_CREATE=false
RUN python -m venv /opt/venv \
    && python -m pip install --disable-pip-version-check poetry==2.5.1
COPY pyproject.toml poetry.lock /opt/project/
WORKDIR /opt/project
RUN poetry install --no-root
COPY --from=markdown /usr/local/bin/node /usr/local/bin/node
COPY --from=markdown /opt/markdown /opt/markdown
ENV PATH="/opt/markdown/node_modules/.bin:/opt/venv/bin:${PATH}"
COPY tests/container/check /opt/check/run
RUN chmod 755 /opt/check/run
WORKDIR /work
