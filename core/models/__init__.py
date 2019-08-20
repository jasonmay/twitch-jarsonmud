from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, text, ForeignKey, BigInteger, Numeric, JSON

Base = declarative_base()


class Entity(Base):
    """
    entity TODO doc
    """

    __tablename__ = "entities"
    id = Column(
        "id", UUID(), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    label = Column(Text)


class EntityProperty(Base):
    """
    entity TODO doc
    """

    __tablename__ = "entity_properties"
    id = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    entity_id = Column("entity_id", UUID(), ForeignKey("entities.id"))
    property_name = Column("property_name", Text)
    property_type = Column("property_type", Text)


class EntityInstance(Base):
    """
    entity TODO doc
    """

    __tablename__ = "entity_instances"
    id = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    entity_id = Column(UUID(), ForeignKey("entities.id"))
    moniker = Column(Text)
    zone = Column(Text)
    tick_time = Column(Numeric())
    tick_variance = Column(Numeric())


class EntityPropertyInstance(Base):
    """
    entity TODO doc
    """

    __tablename__ = "entity_property_instances"
    id = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    entity_instance_id = Column(UUID(), ForeignKey("entity_instances.id"))
    entity_property_id = Column(UUID(), ForeignKey("entity_properties.id"))
    value_uuid = Column(UUID())
    value_str = Column(Text())
    value_int = Column(BigInteger())
    value_numeric = Column(Numeric())
    value_struct = Column(JSON())


class FlagChoice(Base):
    """
    entity TODO doc
    """

    __tablename__ = "flag_choices"
    id = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    entity_property_id = Column(UUID(), ForeignKey("entity_properties.id"))
    flag_value = Column(Text())
