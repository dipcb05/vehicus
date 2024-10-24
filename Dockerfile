# Start with a lightweight Python image
FROM python:3.9-alpine

# Avoid excessive cache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Ensure environment is fully set up and configured
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    build-base \
    postgresql-dev \
    curl \
    && apk add --no-cache bash

# Ensure pip is installed and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Copy .env.example to .env
RUN cp .env.example .env

# Expose the FastAPI server port
EXPOSE 8000

#run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
