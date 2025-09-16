from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.core.infra.events import AbstractEvent


@dataclass(frozen=True)
class StatisticRowAddedEvent(AbstractEvent):
    id: UUID
    created: datetime
    count_requests: int
    subdivision_id: UUID
