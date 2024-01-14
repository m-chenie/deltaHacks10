FROM python:3.8-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.8-slim

# Create a non-root user and switch to it
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache /wheels/* \
    && rm -rf /wheels \
    && rm -rf /usr/src/app

COPY . .
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "-f", "http://localhost:5000/health" ]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
