FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --upgrade pip && pip install .

# The default remains local stdio. This image does not publish a network port.
ENV NEXORA_WORKSPACE=/workspace
RUN useradd --create-home --uid 10001 nexora \
    && mkdir -p /workspace \
    && chown -R nexora:nexora /app /workspace
USER nexora
VOLUME ["/workspace"]
ENTRYPOINT ["nexora-mcp"]
