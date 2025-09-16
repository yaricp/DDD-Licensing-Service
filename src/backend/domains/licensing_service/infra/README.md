# Licensing Service - Infrastructure Layer

This directory contains the infrastructure layer for the Licensing Service. It provides the implementation details for repositories, units of work, adapters, and event/command handlers that interact with external systems and databases. The infrastructure layer follows Domain-Driven Design (DDD) principles and is built to support the domain layer.

## Directory Structure

```
infra/
├── adapters
│   ├── __init__.py
│   ├── kafka_adapter.py
│   ├── orm.py
│   └── user_domain_client.py
├── handlers
│   ├── __init__.py
│   ├── commands
│   │   ├── license.py
│   │   ├── subdivision.py
│   │   ├── tenant.py
│   │   └── user.py
│   └── events
│       ├── license_event_handlers.py
│       ├── outside_broker_event_handlers.py
│       ├── tenant_event_handlers.py
│       └── user_event_handlers.py
├── repos
│   ├── __init__.py
│   └── sqlalchemy
│       ├── license_repo.py
│       ├── subdivision_repo.py
│       ├── tenant_repo.py
│       └── user_repo.py
└── uow
    ├── __init__.py
    └── sqlalchemy
        ├── license_uow.py
        ├── subdivision_uow.py
        ├── tenant_uow.py
        └── user_uow.py
```

## Adapters

- **ORM (`orm.py`)**: Defines SQLAlchemy table mappings and sets up relationships between domain entities like Tenant, Subdivision, License, StatisticRow, and User.
- **Kafka Adapter (`kafka_adapter.py`)**: Handles sending events to an external Kafka message broker.
- **User Domain Client (`user_domain_client.py`)**: Provides integration with the user domain service.

## Repositories

- SQLAlchemy-based implementations of domain repositories.
- Responsible for persisting domain aggregates and entities to the database.
- Examples: `SQLAlchemySubdivisionRepository`, `SQLAlchemyTenantRepository`.

## Units of Work

- Provides transactional boundaries for operations on repositories.
- Implements `SubdivisionUnitOfWork`, `TenantUnitOfWork`, `LicenseUnitOfWork`, etc.
- Ensures all operations within a unit of work are committed or rolled back as a single transaction.

## Handlers

### Command Handlers

- Handle commands from the domain layer.
- Examples: `CreateSubdivisionCommandHandler`, `ActivateSubdivisionLicenseCommandHandler`.
- Delegates command execution to the corresponding service layer.

### Event Handlers

- Handle domain events and optionally forward them to external systems.
- Examples:
  - `ExternalMessageBusSender` sends events to Kafka.
  - `LicenseActivatedEventHandler` handles license activation logic.
  
### Injection

- `COMMANDS_HANDLERS_FOR_INJECTION`: Maps domain commands to their corresponding handlers.
- `EVENTS_HANDLERS_FOR_INJECTION`: Maps domain events to their corresponding event handlers.

## Key Features

- Fully compatible with the domain layer and DDD principles.
- Provides a clean separation of concerns between infrastructure and domain.
- Easily replaceable implementations using dependency injection.
- Supports async operations for database and message bus interactions.
- Implements eager loading of related aggregates to optimize database queries.

## Usage

1. Import the repository or unit of work from the infra layer.
2. Use command/event handlers to interact with the domain layer.
3. All operations are asynchronous and intended to be used with `asyncio`.

## Example

```python
from infra.repos.sqlalchemy.subdivision_repo import SQLAlchemySubdivisionRepository
from infra.uow.sqlalchemy.subdivision_uow import SQLAlchemySubdivisionUnitOfWork

async with SQLAlchemySubdivisionUnitOfWork() as uow:
    subdivisions = await uow.subdivisions.list()
```

This setup ensures that the domain logic remains isolated from persistence, messaging, and external integrations.


🔗 Back to [Backend README](../../../README.md)