from uuid import UUID
from datetime import datetime
from dataclasses import dataclass

from backend.core.infra.events import AbstractEvent


@dataclass(frozen=True)
class StatisticRowAddedEvent(AbstractEvent):
    id: UUID
    created: datetime
    count_requests: int
    subdivision_id: UUID
