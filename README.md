# Debug & Optimize a Broken Containerized App

## Project Overview

This project demonstrates how to debug and optimize a containerized Flask application connected to PostgreSQL using Docker Compose.

The application was intentionally configured with multiple issues and was debugged step by step.

## Technologies

- Docker
- Docker Compose
- Python
- Flask
- PostgreSQL
- Docker Networking
- Docker Health Checks

## Architecture

Browser
   |
   | localhost:8085
   |
Flask Container
   |
   | database:5432
   |
PostgreSQL Container

## Project Structure

Docker-1/
├── app/
│   ├── app.py
│   └── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
└── README.md

## Application

The Flask application provides:

- `/` - Application and database status
- `/health` - Application health check

## Database

PostgreSQL runs inside a Docker container.

The application connects to PostgreSQL using the Docker Compose service name:

database:5432

The PostgreSQL port is not exposed to the host because the application communicates with it through the internal Docker network.

## Debugging Issues

### 1. Dockerfile Path Error

The Compose file originally used:

build: ./app

while the Dockerfile was located in the project root.

Fixed by using:

build: .

### 2. Requirements File Error

The Dockerfile originally copied the entire project and attempted to find requirements.txt at the wrong location.

Fixed by explicitly copying:

COPY app/requirements.txt .

### 3. PostgreSQL Port Conflict

Host port 5432 was already being used by another PostgreSQL Docker container.

The database host port mapping was removed.

The application communicates with PostgreSQL internally using:

database:5432

### 4. Database Configuration Error

The application and PostgreSQL container originally used different passwords.

Both were changed to:

correctpassword

### 5. Database Hostname Error

The application originally used an incorrect database hostname.

The Compose service name is:

database

Therefore:

DB_HOST=database

### 6. Database Readiness

A PostgreSQL health check was added.

The Flask container waits for PostgreSQL to become healthy before starting.

### 7. Application Port Conflict

Host port 8080 was already occupied by another application.

The Flask application is exposed using:

8085:5000

## Running the Application

Build and start:

docker compose up --build -d

Check containers:

docker compose ps

View application logs:

docker compose logs app

View database logs:

docker compose logs database

Open:

http://localhost:8085

Health check:

http://localhost:8085/health

## Optimization

The Docker image was optimized using:

- python:3.12-slim
- pip --no-cache-dir
- Docker layer caching
- .dockerignore
- Pinned Python dependencies
- Health checks
- Internal Docker networking
- Persistent PostgreSQL volume

## Cleanup

To stop the project:

docker compose down

To remove containers and the project network:

docker compose down

To remove the database volume as well:

docker compose down -v