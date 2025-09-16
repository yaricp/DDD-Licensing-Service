from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from backend.core.domain.entity import AbstractEntity


@dataclass
class StatisticRow(AbstractEntity):
    created: datetime
    count_requests: int
    subdivision_id: UUID
    id: Optional[UUID] = None

    @classmethod
    def make(cls, count_requests: int, subdivision_id: UUID) -> StatisticRow:
        return cls(
            created=datetime.now(),
            count_requests=count_requests,
            subdivision_id=subdivision_id,
        )
