# ==========================================
# Stage 1 - Dependency Builder
# ==========================================
FROM python:3.14-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv ${VIRTUAL_ENV}

COPY app/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt


# ==========================================
# Stage 2 - Production Runtime
# ==========================================
FROM python:3.14-slim AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME=cloud-native-platform-api \
    APP_VERSION=1.0.0 \
    ENVIRONMENT=container

RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

COPY --from=builder /opt/venv /opt/venv

COPY --chown=appuser:appgroup app/app.py .

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
