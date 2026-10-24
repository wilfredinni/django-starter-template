FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170 AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

FROM base AS builder

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv export --locked --all-extras --no-emit-project > requirements.txt \
    && uv pip install --prefix=/install --no-cache --require-hashes -r requirements.txt

FROM base AS runtime

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser \
    && chown appuser:appuser /app

COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import http.client; c = http.client.HTTPConnection('127.0.0.1', 8000, timeout=3); c.request('GET', '/'); exit(0 if 200 <= c.getresponse().status < 400 else 1)"
