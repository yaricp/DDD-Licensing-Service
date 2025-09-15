from uuid import uuid4
from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, Boolean,
    UUID, DateTime
)
from sqlalchemy.orm import relationship

from backend.core.infra.database.metadata import mapper_registry


tenants_table = Table(
    "tenants",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    ),
    Column("name", String, nullable=False, unique=True),
    Column("address", String, nullable=False),
    Column("email", String, nullable=False),
    Column("phone", String, nullable=False),
)

lisenses_table = Table(
    "lisenses",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("type", String, nullable=False),
    Column("status", String, nullable=False),
    Column("activated", DateTime, nullable=True),
    Column("expirated", DateTime, nullable=True),
    Column("created", DateTime, nullable=False),
    Column("expiration", DateTime, nullable=True),
    Column("count_requests", Integer, nullable=True),
    Column(
        "subdivision_id", UUID,
        ForeignKey(
            "subdivisions.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
)

subdivisions_table = Table(
    "subdivisions",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("name", String, nullable=False),
    Column("location", String, nullable=False),
    Column("link_to_subdivision_processing_domain", String),
    Column("work_status", String, nullable=False),
    Column(
        "tenant_id", UUID,
        ForeignKey(
            "tenants.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
)

statistic_row_table = Table(
    "statistic_rows",
    mapper_registry.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("created", DateTime, nullable=False),
    Column("count_requests", Integer, nullable=False),
    Column(
        "subdivision_id", UUID,
        ForeignKey("subdivisions.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
)

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("user_id", UUID, primary_key=True, nullable=False, unique=True),
    Column(
        "tenant_id", UUID,
        ForeignKey("tenants.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    ),
    Column("subdivision_id", UUID, nullable=True),
    Column("email", String, nullable=True),
    Column("tg_id", String, nullable=True),
    Column("superadmin", Boolean, default=False)
)


def start_mappers():
    """
    Map all domain models to ORM models,
    for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    print("Start Mapper")
    # Imports here not to ruin alembic logics.
    # Also, only for mappers they needed:
    from ...domain.aggregates.tenant import (
        Tenant
    )
    from ...domain.aggregates.subdivision import (
        Subdivision
    )
    from ...domain.aggregates.entities.stat_row import (
        StatisticRow
    )
    from ...domain.aggregates.entities.license import (
        License
    )
    from ...domain.aggregates.entities.user import (
        User
    )

    mapper_registry.map_imperatively(
        class_=Tenant, local_table=tenants_table,
        properties={
            "users": relationship(
                User,
                back_populates="tenant",
                cascade="all, delete-orphan",
                lazy="selectin"
            ),
            "subdivisions": relationship(
                Subdivision,
                back_populates="tenant",
                cascade="all, delete-orphan",
                lazy="selectin"
            ),
        }
    )
    mapper_registry.map_imperatively(
        class_=Subdivision, local_table=subdivisions_table,
        properties={
            "licenses": relationship(
                License,
                back_populates="subdivision",
                cascade="all, delete-orphan",
                lazy="selectin"
            ),
            "statistics": relationship(
                StatisticRow,
                back_populates="subdivision",
                cascade="all, delete-orphan",
                lazy="selectin"
            ),
            "tenant": relationship(
                Tenant,
                back_populates="subdivisions"
            )
        }
    )
    mapper_registry.map_imperatively(
        class_=StatisticRow,
        local_table=statistic_row_table,
        properties={
            "subdivision": relationship(
                Subdivision,
                back_populates="statistics"
            )
        }
    )
    mapper_registry.map_imperatively(
        class_=License, local_table=lisenses_table,
        properties={
            "subdivision": relationship(
                Subdivision,
                back_populates="licenses"
            )
        }
    )
    mapper_registry.map_imperatively(
        class_=User, local_table=users_table,
        properties={
            "tenant": relationship(
                Tenant,
                back_populates="users"
            )
        }
    )
    print("Finish Mapper")
