from pydantic import BaseModel
from typing import Any, Type, TypeVar, List
from dataclasses import asdict, fields, is_dataclass


T = TypeVar("T", bound=BaseModel)


class BaseMapper:
    @staticmethod
    def to_schema(schema_cls: Type[T], domain_obj: Any) -> T:
        """
        Convert a domain object (dataclass or regular class)
        into a Pydantic schema.
        """
        if is_dataclass(domain_obj):
            data = {}
            for f in fields(domain_obj):
                if f.name.startswith("_"):
                    continue
                value = getattr(domain_obj, f.name)
                if isinstance(value, list):
                    value = [BaseMapper._convert_item(v) for v in value]
                else:
                    value = BaseMapper._convert_item(value)
                data[f.name] = value
            return schema_cls(**data)    
        elif hasattr(domain_obj, "__dict__"):
            data = vars(domain_obj)    # regular class -> dict
        else:
            raise TypeError(
                f"Unsupported domain object type: {type(domain_obj)}"
            )

        return schema_cls(**data)

    @staticmethod
    def _convert_item(domain_obj):
        if is_dataclass(domain_obj):
            data = {}
            for f in fields(domain_obj):
                if f.name.startswith("_"):
                    continue
                value = getattr(domain_obj, f.name)
                if isinstance(value, list):
                    value = [BaseMapper._convert_item(v) for v in value]
                else:
                    value = BaseMapper._convert_item(value)
                data[f.name] = value
            return data
        elif isinstance(domain_obj, list):
            return [BaseMapper._convert_item(v) for v in value]
        else:
            return domain_obj

    @staticmethod
    def list_to_schema(schema_cls: Type[T], domain_objs: List[Any]) -> List[T]:
        """
        Convert a list of domain objects into a list of Pydantic schemas.
        """
        return [BaseMapper.to_schema(schema_cls, obj) for obj in domain_objs]
