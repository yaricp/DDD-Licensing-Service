# Licensing Service Domain Layer

This README describes the **Domain Layer** of the `licensing_service` module following Domain-Driven Design (DDD) principles. It covers the aggregates, value objects, exceptions, services, repositories, and units of work.

---

## Structure

```
domain/
│  __init__.py
│  constants.py
│
├─ aggregates/
│   ├─ __init__.py
│   ├─ subdivision.py
│   ├─ tenant.py
│   └─ entities/
│       ├─ license.py
│       └─ stat_row.py
│
├─ exceptions/
│   ├─ __init__.py
│   ├─ license.py
│   ├─ subdivision.py
│   ├─ statistic_row.py
│   └─ tenant.py
│
├─ value_objects/
│   ├─ __init__.py
│   ├─ email.py
│   ├─ entity_uuid.py
│   ├─ license_status.py
│   ├─ license_type.py
│   └─ work_status.py
│
└─ services/
    ├─ __init__.py
    ├─ commands/
    ├─ events/
    ├─ handlers/
    ├─ repos/
    └─ uow/
```

---

## Aggregates

### Subdivision

- Represents a subdivision within a tenant.
- Contains a list of `License` entities and `StatisticRow` entries.
- Handles business rules, e.g., license activation, deactivation, and statistic row additions.
- Implements methods like `add_license`, `update_license`, `delete_license`, `activate_license`, `deactivate_license`, `save_day_statistic`.
- Uses an `AbstractEventBus` to publish domain events.

### Tenant

- Represents the tenant aggregate.
- Handles tenant-specific business logic.

### Entities

- `License` – business entity representing a license with its properties, status, and operations.
- `StatisticRow` – entity for tracking usage statistics.

---

## Value Objects

- `LicenseType` – enumeration defining license types.
- `WorkStatus` – enumeration for active/inactive status.
- `Email` – value object encapsulating email logic.
- `EntityUUID` – standard UUID wrapper for entities.
- `LicenseStatus` – represents status of a license.

---

## Exceptions

Domain-specific exceptions for enforcing business rules:

- `SubdivisionNotFoundError`
- `LicenseNotFoundError`
- `SubdivisionInactiveError`
- `LicenseInactiveError`
- `SubdivisionStatisticAlreadyExistsError`

These exceptions are used to maintain consistency and enforce invariants in aggregates.

---

## Services

### Command Services

- Encapsulate operations that **change the state** of aggregates.
- Examples: `SubdivisionCommandService`, `LicenseCommandService`.
- Handle domain commands such as `CreateSubdivisionCommand`, `AddStatisticRowCommand`, etc.
- Trigger domain events after state changes.

### Query Services

- Encapsulate operations for **reading aggregate data**.
- Examples: `SubdivisionQuery`.
- Interact with the Unit of Work to fetch data from repositories.

### Domain Event Bus

- Handles publishing and subscription of domain events.
- Ensures that events propagate between aggregates and external services if needed.

### Handlers

- Command Handlers – process commands using Unit of Work and aggregates.
- Event Handlers – react to events for side effects.

---

## Repositories

### SubdivisionRepository

- Abstract repository interface defining methods for:
  - `add`, `get`, `update`, `save`, `delete`, `list`
  - `get_license_by_id`, `add_statistic_row`
- Allows implementation substitution without changing the service layer.
- Used by Unit of Work implementations.

### Other Repositories

- TenantRepository, LicenseRepository – similar abstraction for respective aggregates.

---

## Unit of Work (UoW)

### SubdivisionUnitOfWork

- Abstract class defining the transactional boundary for subdivisions.
- Provides access to `SubdivisionRepository`.
- Ensures that operations on aggregates are committed atomically.

### General Principles

- Implements the **Unit of Work pattern** for atomic operations.
- Provides dependency injection to replace repository implementations easily.
- Works asynchronously to support high concurrency.

---

## Key Concepts

- **DDD Principles**: Aggregates, Entities, Value Objects, Repositories, Services, Events.
- **CQRS**: Separation of Command and Query services.
- **Event Sourcing**: Domain events are used to represent state changes.
- **Unit of Work**: Ensures transactional consistency across repositories.
- **Asynchronous Operations**: All service and repository methods support async/await.

---

This domain layer forms the **core of the licensing_service**, implementing all business rules and protecting the integrity of aggregates according to DDD standards.


🔗 Back to [Backend README](../../../README.md)