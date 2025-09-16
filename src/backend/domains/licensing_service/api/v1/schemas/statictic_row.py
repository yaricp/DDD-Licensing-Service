from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StatisticRowBase(BaseModel):
    subdivision_id: UUID
    count_requests: int
    created: datetime


class StatisticRowCreate(BaseModel):
    count_requests: int


class StatisticRow(StatisticRowBase):
    pass
