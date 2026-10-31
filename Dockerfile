# ==============================================================================
# DataSetu (डेटासेतु) - Production Container
# Autonomous National Open Data to Open API Engine
# ==============================================================================

# Build Stage
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY datasetu/ ./datasetu/

RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels .

# Runtime Stage
FROM python:3.11-slim AS runner

WORKDIR /app

# Create non-privileged service user
RUN groupadd -r datasetu && useradd -r -g datasetu -u 1001 datasetu

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/wheels /wheels
COPY pyproject.toml README.md ./
COPY datasetu/ ./datasetu/
COPY demo/ ./demo/
COPY benchmark/ ./benchmark/

RUN pip install --no-cache-dir /wheels/* && \
    pip install --no-cache-dir -e . && \
    rm -rf /wheels

# Set permissions for non-root execution
RUN chown -R datasetu:datasetu /app
USER datasetu

# Expose standard REST API port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Built-in health check
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Default execution: serve bundled master dataset
CMD ["datasetu", "serve", "demo/bharat_governance_master_2026.csv", "--host", "0.0.0.0", "--port", "8000"]
