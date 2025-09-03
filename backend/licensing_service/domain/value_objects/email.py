from __future__ import annotations
from dataclasses import dataclass
from pydantic import Field

from backend.core.domain.value_object import ValueObject

EmailType = Field(
    pattern=r"\([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


@dataclass(slots=True)
class Email(ValueObject):
    email: EmailType

    def __composite_values__(self):
        return self.email
