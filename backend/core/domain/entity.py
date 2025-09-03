from abc import ABC
from uuid import UUID
from dataclasses import field, dataclass, asdict
from typing import Generic, Optional, Any, Dict, Set, TypeVar

from .value_object import GenericUUID


# EntityType = TypeVar("EntityType", bound="Entity")
EntityId = TypeVar("EntityId", bound="GenericUUID")


@dataclass
class AbstractEntity(ABC):
    """
    Base model, from which any domain model should be inherited.
    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    async def to_dict(
        self,
        exclude: Optional[Set[str]] = None,
        include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
