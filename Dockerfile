FROM python:3.11-slim

LABEL maintainer="Nik Jois <nikjois@llamasearch.ai>"
LABEL description="OpenGov-WaterfrontEngineering: Marine/waterfront screening toolkit"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY pyproject.toml tox.ini ./
COPY src/ src/
COPY tests/ tests/

RUN pip install --upgrade pip && \
    pip install -e . && \
    pip install pytest pytest-asyncio pytest-cov

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=5)" || exit 1

CMD ["python", "-m", "open_gov_waterfront.server"]
