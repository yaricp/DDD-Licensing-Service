# DDD Licensing Service – Monorepo

This repository contains a set of services built with a **Domain-Driven Design (DDD)** approach.  
The services are orchestrated via `docker-compose` and can be built and run locally with a single command.

## Services

- [Backend](./src/backend/README.md) — Main API service, implements multiple bounded contexts (domains).  
- [Email Channel](./src/email_channel/README.md) — Service for processing and sending email notifications.  
- [Telegram Channel](./src/telegram_channel/README.md) — Telegram integration service.  

## Project Structure

```
.
├── src/
│   ├── backend/          # API + domains + shared infrastructure (docker container)
│   ├── email_channel/    # email notification service (docker container)
│   ├── telegram_channel/ # Telegram integration service (docker container)
│   └── protobuf_types/   # Protobuf schemas and generated types
├── scripts/              # Utility scripts (build, tests, etc.)
├── docker-compose.yml
└── ...
```

## Scripts

- `scripts/build_images.sh` — builds Docker images for all services.  
- `scripts/start_test_backend.sh` — runs backend tests inside Docker.  

## How to Run

### Build and start the entire project
```bash
docker-compose up -d
```

### Build images separately
```bash
./scripts/build_images.sh
```

### Run backend tests
```bash
./scripts/start_test_backend.sh
```
