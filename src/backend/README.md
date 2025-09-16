# Backend Service

The **Backend Service** is the core API of the system, built using **Domain-Driven Design (DDD)** principles.  
It exposes endpoints for multiple bounded contexts (domains) and provides a unified API layer.

## Structure

```
backend/
├── domains/                # Bounded contexts (domains)
│   └── licensing_service/  # Example: Licensing domain
│       ├── api/            # HTTP/gRPC endpoints
│       ├── app/            # Application services (use cases)
│       ├── domain/         # Pure domain layer (aggregates, entities, VOs, events)
│       ├── infra/          # Infrastructure (repositories, adapters)
│       └── tests/          # Unit and integration tests
├── infrastructure/         # Shared infrastructure for all domains
│   ├── alembic/            # Alembic migrations
│   ├── rest_api/           # RestAPI for all domains
│   └── ...
├── config.py               # Global configuration
├── main.py                 # FastAPI entry point
└── ...
```

## Key Points

- **Domain isolation**: each bounded context (domain) is self-contained, with its own endpoints, adapters, and infrastructure.  
- **Shared infrastructure**: cross-domain components (database, messaging, monitoring, etc.) live in `infrastructure/`.  
- **DDD layers**:  
  - `domain/` contains pure business logic.  
  - [app/](./domains/licensing_service/app/README.md) contains use cases (application services).  
  - `infra/` implements persistence and integration.  


---

🔗 Back to [Root README](../../README.md)
