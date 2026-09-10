# Docker Learning App

Small learning project built to practice Docker with a multi-container architecture.

## Stack

- Python
- Flask
- PostgreSQL
- pgAdmin
- Docker
- Docker Compose

## Architecture

The project runs three services:

- `app`: Flask web application
- `db`: PostgreSQL database
- `pgadmin`: database administration interface

## Features

- Add names to PostgreSQL
- Search how many people have a given name
- Persistent PostgreSQL data with Docker volumes
- Persistent pgAdmin configuration
- Container-to-container networking with Docker Compose

## Run

```bash
docker compose up --build
```

## Access

App:

http://localhost:5000

pgAdmin:

http://localhost:8080

## Docker concepts demonstrated

- Custom Docker image
- Dockerfile
- Docker Compose
- Multi-container applications
- Docker networking
- PostgreSQL container
- Persistent volumes
- Port mapping