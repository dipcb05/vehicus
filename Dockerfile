#alpine is so lightweight
FROM python:3.9-alpine

# avoid accessive cache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# ensure environment is fully setup and configured
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    build-base \
    postgresql-dev \
    curl \
    && apk add --no-cache bash

# ensured pip is installed and installing dependencies

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


#copying application code into the container, to app folder, because workdir is /app
COPY . .

RUN cp .env.example .env

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
