# Stage 1: Build frontend
FROM node:22-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run generate

# Stage 2: Final stage with Python and frontend ------------------------------------------------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy backend requirements and install dependencies
COPY backend/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend code
COPY backend /app/backend


# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/.output/public/ /app/static/


WORKDIR /app/backend

RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Create MIME types file directly in the container
RUN echo "application/javascript js\napplication/javascript mjs\ntext/javascript js\ntext/javascript mjs\ntext/css css" > /app/mime.types


# TODO uvicorn ...