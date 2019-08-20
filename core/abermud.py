from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Entity,
    EntityProperty,
    EntityInstance,
    EntityPropertyInstance,
    FlagChoice,
)
import json

with open("zones.json", "r") as z:
    aber = json.load(z)

ENTITIES = ["location", "object", "mobile", "quest", "currency", "spell"]

entity_records = {}


def add_entities(session):
    added = False
    for entity_value in ENTITIES:
        entity = session.query(Entity).filter(Entity.label == entity_value)
        if not entity.count():
            added = True
            session.add(Entity(label=entity_value))
        else:
            entity_records[entity_value] = entity.first()

    if added:
        session.commit()


def populate_entity_records(session):
    for entity_value in ENTITIES:
        if entity_value not in entity_records:
            entity = session.query(Entity).filter(Entity.label == entity_value).first()
            entity_records[entity_value] = entity


def add_entity_location_properties(session):
    added = False
    type_map = {"altitude": "integer", "flags": "flags"}
    location_entity_id = entity_records["location"].id
    for propname, proptype in type_map.items():
        prop = session.query(EntityProperty).filter(
            EntityProperty.property_name == propname
        )
        if not prop.count():
            added = True
            session.add(
                EntityProperty(
                    entity_id=location_entity_id,
                    property_name=propname,
                    property_type=proptype,
                )
            )

    if added:
        session.commit()


def add_entity_location_properties(session):
    added = False
    type_map = {"altitude": "integer", "flags": "flags"}
    location_entity_id = entity_records["location"].id
    for propname, proptype in type_map.items():
        prop = session.query(EntityProperty).filter(
            EntityProperty.property_name == propname
        )
        if not prop.count():
            added = True
            session.add(
                EntityProperty(
                    entity_id=location_entity_id,
                    property_name=propname,
                    property_type=proptype,
                )
            )

    if added:
        session.commit()


if __name__ == "__main__":
    # TODO put in env var
    engine = create_engine("postgresql://postgres:jarsonmud@storage:5432/postgres")
    Session = sessionmaker(bind=engine)
    session = Session()
    add_entities(session)
    populate_entity_records(session)
    add_entity_location_properties(session)
