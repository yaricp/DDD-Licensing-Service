# Application Layer - Licensing Service

This folder represents the **Application Layer** of the `licensing_service` domain, following the principles of Domain-Driven Design (DDD) and the CQRS pattern.

The application layer is responsible for coordinating the execution of domain logic through **commands**, **queries**, and **services**, without containing business rules itself. It acts as a bridge between the domain model and the outside world (e.g., API, message bus).

## Structure

```
app/
├── commands/   # Application command use cases
├── queries/    # Read-only queries (CQRS)
└── services/   # Application services that orchestrate domain and infra
```

### 1. Commands

Located in: `app/commands/`

Command use cases wrap domain **command objects** and delegate their execution to the global `MessageBusHandler`.  
Example: `SubdivisionCommandUseCase` orchestrates subdivision-related commands such as:

- `create_subdivision`
- `update_subdivision`
- `delete_subdivision`
- `subdivision_add_stat_row`
- `subdivision_create_license`
- `subdivision_update_license`
- `subdivision_delete_license`
- `active_subdivision_license`
- `deactive_subdivision_license`

These classes **do not contain business logic**, but instead build command objects and pass them to the domain for execution.

### 2. Queries

Located in: `app/queries/`

Query classes provide **read-only access** to aggregates, following the CQRS paradigm.  
Example: `SubdivisionQuery` can:

- Fetch a subdivision by ID (`get_subdivision_by_id`)
- Fetch via service delegation (`get_subdivision`)
- List all subdivisions (`get_all_subdivisions`)

Queries directly interact with repositories and services, but never modify the state.

### 3. Services

Located in: `app/services/`

Application services orchestrate **unit of work (UOW)** and coordinate domain logic with infrastructure concerns.  
Example: `SubdivisionService` provides:

- License lifecycle operations (`add_license`, `update_license`, `delete_license`, `activate_subdivision_license`, `deactivate_subdivision_license`)
- Subdivision lifecycle operations (`create_subdivision`, `update_subdivision`, `delete_subdivision`)
- Statistics handling (`add_subdivision_statistic_row`)
- Queries (`get_all_subdivisions`, `get_subdivision_by_id`)

These services:

- Use **UOW (`SQLAlchemySubdivisionUnitOfWork`)** to persist aggregates.
- Trigger **domain events** (e.g., `SubdivisionCreatedEvent`, `LicenseActivatedEvent`) and propagate them to the **infrastructure event bus**.

---

## Example Usage

```python
from backend.domains.licensing_service.app.commands.subdivision_commands import SubdivisionCommandUseCase
from backend.core.messagebus_handler import GlobalMessageBusHandler

messagebus = GlobalMessageBusHandler()
use_case = SubdivisionCommandUseCase(messagebus_handler=messagebus)

# Example: create a subdivision
await use_case.create_subdivision(
    name="Main Branch",
    location="New York",
    tenant_id="...some-uuid..."
)
```

---

## Key Points

- The **Application Layer** has no business rules — only orchestration.  
- **Commands** = intent to change state.  
- **Queries** = read-only operations.  
- **Services** = coordinate domain, infrastructure, and events.  
- Relies on **Unit of Work** and **Message Bus** for transaction management and event propagation.

🔗 Back to [Backend README](../../../README.md)