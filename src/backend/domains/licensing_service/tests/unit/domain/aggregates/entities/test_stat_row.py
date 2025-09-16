# tests/test_statistic_row.py

from datetime import datetime, timedelta
from uuid import uuid4

from backend.domains.licensing_service.domain.aggregates.entities.stat_row import (
    StatisticRow,
)


def test_make_creates_statistic_row():
    subdivision_id = uuid4()
    count_requests = 10

    stat_row = StatisticRow.make(
        count_requests=count_requests, subdivision_id=subdivision_id
    )

    assert stat_row.subdivision_id == subdivision_id
    assert stat_row.count_requests == count_requests
    assert isinstance(stat_row.created, datetime)
    assert stat_row.id is None

    now = datetime.now()
    assert now - timedelta(seconds=1) <= stat_row.created <= now + timedelta(seconds=1)
