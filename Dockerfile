# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv

WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install .

FROM python:3.13-slim AS evaluator

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 10001 evaluator \
    && useradd --uid 10001 --gid evaluator --no-create-home \
        --shell /usr/sbin/nologin evaluator

COPY --from=builder /opt/venv /opt/venv

WORKDIR /workspace
COPY tests ./tests
RUN mkdir artifacts && chown -R evaluator:evaluator /workspace

USER 10001:10001

CMD ["evaluate-scenarios", "--output", "artifacts/evaluation-report.json"]
