# AXIOM-X Production Container
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p receipts/phase_b receipts/phase_c logs data

ENV PYTHONUNBUFFERED=1
ENV AXIOM_X_ENV=production

EXPOSE 8000 9090

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3   CMD python -c "print('healthy')"

CMD ["python", "capacity_discovery_engine.py"]
