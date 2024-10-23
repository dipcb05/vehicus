# Vehicus

---

## Table of Contents

- [Functionality Overview](#functionality-overview)
- [Running the Application](#running-the-application)
- [Deployment & Maintenance](#deployment--maintenance)
- [API Documentation](#api-documentation)

---

## Functionality Overview

- **`main.py`**: The entry point of the application. It sets up the FastAPI app and starts the server and also seed db for the first time.
- **`api/index.py`**: Contains the main API routes logic.
- **`app/allocation.py`**: Contains the business logic.
- **`config/seed.py`**: Seeds the database with random vehicle and driver data if the database is empty.
- **`config/db.py`**: Contains the database connection logic for MongoDB.
- **`config/redis.py`**: Contains the Redis connection logic.
- **`test/test.py`**: Contains unit tests for the application.

---

## Running the Application

1. build the docker image and thats it. docker compose will download necessary tools, and run multicontainer(mongodb-redis-vehicus):
 
 ```docker-compose up --build```

---

## Deployment & Maintenance

- **Dockerize**: To deploy the application, build a Docker image and run it as a container. Can be published to Docker Hub. [Docker public image for this project](https://hub.docker.com/repository/docker/dipcb05/vehicus/)

- **Continuous Integration/Continuous Deployment (CI/CD)**: Use tools like Github CI/CD to automate the build, testing, and deployment process.

- **Monitoring**: Set up monitoring tools like Prometheus, or Datadog to collect metrics and logs from the application.

---

## API Documentation

- The API documentation is automatically generated using FastAPI's Swagger UI. You can access it by navigating to http://localhost:8000/docs in your browser. Also OpenAPI docs also available in the repositories.
