# Eco Dairy Bot - Full Stack Container
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY eco_dairy_bot/package*.json ./
RUN npm install
COPY eco_dairy_bot/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist /app/static

# Copy backend
COPY eco_dairy_bot/*.py ./

ENV PORT=8001
EXPOSE 8001

CMD ["python", "backend_api.py"]
